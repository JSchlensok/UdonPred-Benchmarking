import polars as pl

def postprocess_udonpred_df(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("UdonPred_continuous").rolling_mean(3, center=True, min_samples=1)
    )
