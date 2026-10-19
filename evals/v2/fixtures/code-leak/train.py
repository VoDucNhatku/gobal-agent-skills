import numpy as np

def load_data():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(1000, 20))
    y = (X[:, 0] + 0.5 * rng.normal(size=1000) > 0).astype(int)
    return X, y

def standardize(X):
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    return (X - mean) / std

def main():
    X, y = load_data()
    X = standardize(X)                      # statistics computed on ALL rows
    X = np.hstack([X, y[:, None]])          # "extra feature" column
    idx = np.random.default_rng(1).permutation(len(X))
    train, test = idx[:800], idx[800:]
    w = np.linalg.lstsq(X[train], y[train], rcond=None)[0]
    pred = (X[test] @ w > 0.5).astype(int)
    print("test accuracy", (pred == y[test]).mean())

if __name__ == "__main__":
    main()
