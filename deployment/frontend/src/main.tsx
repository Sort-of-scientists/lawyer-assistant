import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from 'deployment/frontend/src/app/App.tsx';
import 'normalize.css';
import 'deployment/frontend/src/index.css';
import { Provider } from 'react-redux';
import { store } from 'deployment/frontend/src/store/store.ts';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>,
);
