import 'deployment/frontend/src/app/App.css';
import { withProviders } from 'deployment/frontend/src/app/providers/with-providers.ts';
import { MainRouter } from 'deployment/frontend/src/pages/MainRouter.tsx';
import { ConfigProvider, theme } from 'antd';
import { useThemeWatcher } from 'deployment/frontend/src/entities/hocs/useThemeWatcher.tsx';
import { useAppSelector } from 'deployment/frontend/src/store/hooks/redux.hook.ts';
import { themeObject } from 'deployment/frontend/src/app/styles/theme/theme-variables.ts';
import GlobalStyle from 'deployment/frontend/src/app/styles/global-styles.ts';
function App() {
  const reduxTheme = useAppSelector(state => state.theme.theme);
  useThemeWatcher();
  return (
    <>
      <meta name="theme-color" content={themeObject[reduxTheme].primary} />
      <GlobalStyle />
      <ConfigProvider
        theme={{
          algorithm: reduxTheme !== 'light' ? theme.darkAlgorithm : theme.defaultAlgorithm,
        }}
      >
        <MainRouter />
      </ConfigProvider>
    </>
  );
}

const EnhancedApp = withProviders(App);
export default EnhancedApp;
