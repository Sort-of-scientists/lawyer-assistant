import React, { type ReactElement } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { DOCUMENTS, EDITOR, MAIN, ROOT } from 'deployment/frontend/src/shared/constants/paths.ts';
import { MainLayout } from 'deployment/frontend/src/widgets/main-layout/MainLayout.tsx';
import { MainPage } from 'deployment/frontend/src/pages/page/main/MainPage.tsx';
import { DocumentPage } from 'deployment/frontend/src/pages/page/documents/DocumentPage.tsx';
import { EditorPage } from 'deployment/frontend/src/pages/page/editor/EditorPage.tsx';

export const MainRouter = (): ReactElement => {
  return (
    <Routes>
      <Route path={ROOT} element={<MainLayout />}>
        <Route path={MAIN} element={<MainPage />} />
        <Route path={DOCUMENTS} element={<DocumentPage />} />
        <Route path={EDITOR} element={<EditorPage />} />

        <Route path={ROOT} element={<Navigate to={DOCUMENTS} />} />
      </Route>

      <Route path="*" element={<Navigate to={MAIN} />} />
    </Routes>
  );
};
