from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import sys
import zipfile

import numpy as np
import pandas as pd


VERSION = 'zapas-week3-v1.0'
KEYS = ['Store ID', 'Product ID']
REQUIRED = ['Date', 'Store ID', 'Product ID', 'Category', 'Region',
            'Inventory Level', 'Units Sold', 'Units Ordered', 'Demand Forecast',
            'Price', 'Discount', 'Weather Condition', 'Holiday/Promotion',
            'Competitor Pricing', 'Seasonality']
FEATURES = ['lag_1', 'lag_2', 'lag_3', 'lag_12', 'rolling_mean_3',
            'rolling_mean_6', 'sales_trend', 'month_number']
CONFIG = {'pathway': 'F', 'time_column': 'Date', 'frequency': 'MS',
          'keys': KEYS, 'invalid_key_policy': 'stop', 'duplicate_key_policy': 'stop',
          'missing_sales_policy': 'preserve_and_flag', 'category_filter': None,
          'forecast_horizon_months': 1, 'minimum_history_months': 3}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False,
                                    allow_nan=False) + '\n', encoding='utf-8')


def select_source(raw_dir):
    raw_dir = Path(raw_dir)
    source = raw_dir / 'retail_store_inventory.csv'
    if source.is_file():
        return source
    candidates = []
    for archive in sorted(raw_dir.glob('*.zip')):
        with zipfile.ZipFile(archive) as bundle:
            candidates.extend((archive, item.filename) for item in bundle.infolist()
                              if Path(item.filename).name == source.name)
    if len(candidates) != 1:
        raise ValueError('Upload exactly one retail_store_inventory.csv or ZIP containing it into data/raw.')
    archive, member = candidates[0]
    with zipfile.ZipFile(archive) as bundle:
        source.write_bytes(bundle.read(member))
    return source


def inspect_source(source):
    frame = pd.read_csv(source)
    if frame.empty or not set(REQUIRED).issubset(frame.columns):
        raise ValueError('Empty source or missing required columns.')
    dates = pd.to_datetime(frame['Date'], format='%Y-%m-%d', errors='coerce')
    if dates.isna().any() or frame[KEYS].isna().any().any():
        raise ValueError('Invalid date or missing series identifier; source preserved, pipeline stopped.')
    if frame.duplicated(['Date'] + KEYS).any():
        raise ValueError('Duplicate store/product/day key; resolve source ambiguity before aggregation.')
    sales = pd.to_numeric(frame['Units Sold'], errors='coerce')
    if (frame['Units Sold'].notna() & sales.isna()).any() or (sales.dropna() < 0).any() or np.isinf(sales.dropna()).any():
        raise ValueError('Units Sold must be finite nonnegative numbers or explicit missing values.')
    if not sales.dropna().mod(1).eq(0).all():
        raise ValueError('Units Sold must contain whole-unit counts.')
    frame['Date'] = dates
    frame['Units Sold'] = sales
    report = {'rows': len(frame), 'columns': list(frame.columns),
              'dtypes': {column: str(dtype) for column, dtype in frame.dtypes.items()},
              'missing_by_column': frame.isna().sum().astype(int).to_dict(),
              'date_start': str(dates.min().date()), 'date_end': str(dates.max().date()),
              'stores': int(frame['Store ID'].nunique()),
              'products': int(frame['Product ID'].nunique()),
              'series': len(frame[KEYS].drop_duplicates()),
              'categories': sorted(frame.Category.dropna().unique().tolist()),
              'duplicate_daily_keys': 0, 'invalid_timestamps': 0,
              'products_with_multiple_categories': int((frame.groupby('Product ID').Category.nunique() > 1).sum()),
              'stores_with_multiple_regions': int((frame.groupby('Store ID').Region.nunique() > 1).sum())}
    return frame, report


def prepare(frame):
    daily = frame.sort_values(['Date'] + KEYS, kind='stable').reset_index(drop=True)
    observed = daily.assign(month=daily.Date.dt.to_period('M').dt.to_timestamp())
    grouped = observed.groupby(KEYS + ['month'], sort=True)
    monthly = grouped.agg(observed_days=('Date', 'nunique'),
                          nonmissing_sales_days=('Units Sold', 'count'),
                          units_sold=('Units Sold', lambda values: values.sum(min_count=1)),
                          inventory_last_observed=('Inventory Level', lambda values: values.iloc[-1]),
                          last_observed_date=('Date', 'max'),
                          category_count=('Category', 'nunique'),
                          region_count=('Region', 'nunique')).reset_index()
    calendar = pd.date_range(observed.month.min(), observed.month.max(), freq='MS')
    grid = observed[KEYS].drop_duplicates().merge(pd.DataFrame({'month': calendar}), how='cross')
    monthly = grid.merge(monthly, on=KEYS + ['month'], how='left', validate='one_to_one')
    monthly = monthly.sort_values(KEYS + ['month']).reset_index(drop=True)
    monthly['observed_days'] = monthly.observed_days.fillna(0).astype(int)
    monthly['nonmissing_sales_days'] = monthly.nonmissing_sales_days.fillna(0).astype(int)
    monthly['expected_days'] = monthly.month.dt.days_in_month
    monthly['complete_month'] = ((monthly.observed_days == monthly.expected_days) &
                                 (monthly.nonmissing_sales_days == monthly.expected_days))
    monthly['target_units_sold'] = monthly.units_sold.where(monthly.complete_month)
    monthly['month_number'] = monthly.month.dt.month
    series = monthly.groupby(KEYS, sort=False)['target_units_sold']
    for lag in [1, 2, 3, 12]:
        monthly[f'lag_{lag}'] = series.shift(lag)
    for window in [3, 6]:
        monthly[f'rolling_mean_{window}'] = series.transform(
            lambda values: values.shift(1).rolling(window, min_periods=window).mean())
    monthly['sales_trend'] = monthly.lag_1 - monthly.lag_2
    monthly['history_ready'] = monthly[['lag_1', 'lag_2', 'lag_3']].notna().all(axis=1)
    monthly['eligible_for_training'] = monthly.complete_month & monthly.history_ready
    monthly['split'] = 'ineligible'
    eligible_months = sorted(monthly.loc[monthly.eligible_for_training, 'month'].unique())
    if len(eligible_months) >= 7:
        train_end, validation_end = eligible_months[-7], eligible_months[-4]
        eligible = monthly.eligible_for_training
        monthly.loc[eligible & (monthly.month <= train_end), 'split'] = 'train'
        monthly.loc[eligible & (monthly.month > train_end) & (monthly.month <= validation_end), 'split'] = 'validation'
        monthly.loc[eligible & (monthly.month > validation_end), 'split'] = 'test'
    else:
        monthly.loc[monthly.eligible_for_training, 'split'] = 'train'
    return daily, monthly


def export_and_validate(source, destination, base):
    destination, base = Path(destination), Path(base)
    frame, inspection = inspect_source(source)
    daily, monthly = prepare(frame)
    destination.mkdir(parents=True, exist_ok=True)
    outputs = []
    for filename, result in [('prepared_timeseries.csv', daily), ('monthly_sales_features.csv', monthly)]:
        path = destination / filename
        result.to_csv(path, index=False, date_format='%Y-%m-%d', lineterminator='\n')
        loaded = pd.read_csv(path)
        expected = result.copy()
        for column in expected.select_dtypes(include=['datetime']).columns:
            expected[column] = expected[column].dt.strftime('%Y-%m-%d')
        pd.testing.assert_frame_equal(loaded, expected, check_dtype=False, check_exact=False)
        outputs.append(path)
    if len(daily) != len(frame) or list(daily.columns) != list(frame.columns):
        raise AssertionError('Daily export lost rows or columns.')
    if not daily.Date.is_monotonic_increasing or monthly.duplicated(KEYS + ['month']).any():
        raise AssertionError('Invalid ordering or monthly uniqueness.')
    if not np.isclose(daily['Units Sold'].sum(), monthly.units_sold.sum()):
        raise AssertionError('Monthly totals do not reconcile to raw sales.')
    if set(map(tuple, daily[KEYS].to_numpy())) != set(map(tuple, monthly[KEYS].to_numpy())):
        raise AssertionError('Store/product series were lost.')
    if monthly.loc[~monthly.complete_month, 'target_units_sold'].notna().any():
        raise AssertionError('Incomplete month exposed as a training target.')
    inspection.update({'monthly_rows': len(monthly),
                       'complete_month_rows': int(monthly.complete_month.sum()),
                       'incomplete_month_rows': int((~monthly.complete_month).sum()),
                       'eligible_rows': int(monthly.eligible_for_training.sum()),
                       'split_counts': monthly.split.value_counts().to_dict(),
                       'total_units_sold': int(daily['Units Sold'].sum()),
                       'raw_preserved': True, 'validation': 'PASS'})
    quality = destination / 'validation_report.json'
    write_json(quality, inspection)
    outputs.append(quality)
    return outputs, inspection


def run_pipeline(base, stage='pipeline_v1/timeseries'):
    base = Path(base).resolve()
    source = select_source(base / 'data/raw')
    before = sha256_file(source)
    destination = base / 'data' / stage
    outputs, inspection = export_and_validate(source, destination, base)
    if before != sha256_file(source):
        raise AssertionError('Raw source changed.')
    records = [{'source_id': 'S01', 'source_filename': 'retail_store_inventory.csv',
                'source_sha256': before, 'source_size_bytes': source.stat().st_size,
                'prepared_output': path.relative_to(base).as_posix(),
                'prepared_sha256': sha256_file(path), 'size_bytes': path.stat().st_size,
                'processing_note': CONFIG, 'source_version': 'Local file fingerprint',
                'access_rights': 'Dataset licence not verified; confirm before public redistribution'}
               for path in outputs]
    manifest = {'pipeline_version': VERSION, 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
                'runtime': {'python': platform.python_version(), 'pandas': pd.__version__, 'numpy': np.__version__},
                'records': records, 'inspection': inspection, 'model_feature_allowlist': FEATURES,
                'source_output_mapping': [{'source': 'data/raw/retail_store_inventory.csv',
                                           'output': record['prepared_output']} for record in records]}
    manifest_path = base / 'data/week3_manifest.json' if stage == 'processed' else destination / 'pipeline_manifest.json'
    write_json(manifest_path, manifest)
    print(f'SUCCESS: {stage}: {inspection["rows"]} daily rows; {inspection["monthly_rows"]} monthly rows')
    return manifest


def verify_repeatability(first, second):
    for key in ['records', 'inspection', 'source_output_mapping', 'model_feature_allowlist']:
        if first[key] != second[key]:
            raise AssertionError(f'Repeatability failed: {key}')
    return {'status': 'PASS', 'checks': ['source hashes and sizes', 'output hashes and sizes',
                                       'counts', 'source-output mappings', 'feature allowlist'],
            'scope': 'Same-runtime repeatability; execution timestamps intentionally excluded'}


if __name__ == '__main__':
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    run_pipeline(base, 'processed')
    first = run_pipeline(base)
    second = run_pipeline(base)
    write_json(base / 'data/pipeline_v1/timeseries/repeatability_report.json', verify_repeatability(first, second))
