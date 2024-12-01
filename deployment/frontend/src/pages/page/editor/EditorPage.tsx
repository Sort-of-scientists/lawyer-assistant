import React, { type ReactElement } from 'react';
import { DocEditor } from '@/widgets/editor/DocEditor.tsx';

export const EditorPage = (): ReactElement => {
  console.log(`${import.meta.env.VITE_API_URL}/get-test-file`);

  const fileId = localStorage.getItem('fileId');
  return (
    <>
      <DocEditor fileUrl={`${import.meta.env.VITE_API_URL}/download?document_id=${fileId}`} />
    </>
  );
};
