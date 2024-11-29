import React, { type ReactElement } from 'react';
import { PageTitle } from 'deployment/frontend/src/features/page-title/PageTitle.tsx';
import { MainPageInfo } from 'deployment/frontend/src/widgets/main-page-info/MainPageInfo.tsx';

export const MainPage = (): ReactElement => {
  return (
    <>
      <PageTitle>Главная</PageTitle>
      <MainPageInfo />
    </>
  );
};
