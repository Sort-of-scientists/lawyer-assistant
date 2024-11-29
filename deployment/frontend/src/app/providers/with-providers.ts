import compose from 'compose-function';
import { withRouter } from 'deployment/frontend/src/app/providers/BrowserRouter.tsx';

export const withProviders = compose(withRouter);
