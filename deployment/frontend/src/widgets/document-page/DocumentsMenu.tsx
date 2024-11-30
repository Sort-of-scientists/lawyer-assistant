import React, { type ReactElement } from 'react';
import { DocumentElement } from '@/features/elemet/DocumentElement.tsx';
import styled from 'styled-components';
import { documentData } from '@/shared/data/document.data.ts';

export const DocumentsMenu = (): ReactElement => {
  return (
    <Wrapper>
      {documentData.map(elem => (
        <DocumentElement key={elem.id} elem={elem} />
      ))}
    </Wrapper>
  );
};

const Wrapper = styled.div`
  width: 100%;
  height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  row-gap: 20px;
  overflow-y: auto;
`;
