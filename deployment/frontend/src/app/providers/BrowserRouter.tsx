import { type ReactNode, Suspense } from 'react';
import { BrowserRouter } from 'react-router-dom';

export const withRouter = (component: () => ReactNode) => () => (
  <BrowserRouter>
    <Suspense fallback="Loading...">{component()}</Suspense>
  </BrowserRouter>
);
