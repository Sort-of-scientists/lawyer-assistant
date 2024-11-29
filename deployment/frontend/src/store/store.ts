import { errorLoggingMiddleware } from 'deployment/frontend/src/store/middlewares/errorLogging.middleware';
import { configureStore } from '@reduxjs/toolkit';
import rootReducer from 'deployment/frontend/src/store/reducers';

export const store = configureStore({
  reducer: rootReducer,
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({ serializableCheck: false }).concat(errorLoggingMiddleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
