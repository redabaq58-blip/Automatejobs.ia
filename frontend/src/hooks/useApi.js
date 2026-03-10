import { useState, useEffect, useCallback } from 'react';

export function useApi(apiFn, initialParams = [], deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetch = useCallback(async (...params) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFn(...params);
      setData(result);
      return result;
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || 'Failed to load data');
      return null;
    } finally {
      setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    fetch(...initialParams);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { data, loading, error, refetch: fetch };
}

export function useApiLazy(apiFn) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...params) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFn(...params);
      setData(result);
      return result;
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || 'Failed');
      return null;
    } finally {
      setLoading(false);
    }
  }, [apiFn]);

  return { data, loading, error, execute };
}
