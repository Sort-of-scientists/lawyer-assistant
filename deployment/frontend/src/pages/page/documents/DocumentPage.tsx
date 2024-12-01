import React, { type ReactElement, useState } from 'react';
import { PageTitle } from '@/features/page-title/PageTitle.tsx';
import { DocumentsMenu } from '@/widgets/document-page/DocumentsMenu.tsx';
import styled from 'styled-components';
import { SearchOutlined } from '@ant-design/icons';
import {
  DocumentTypeSelect,
  IChooseFileType,
} from '@/widgets/document-type/DocumentTypeSelect.tsx';

export const DocumentPage = (): ReactElement => {
  const [chooseFileType, setChooseFileType] = useState<IChooseFileType>({ value: 'Выберете тип' });
  return (
    <>
      <PageTitle>Документы</PageTitle>
      <Container>
        <Wrapper>
          <Title>Ваши документы</Title>
          <FilterContainer>
            <DocumentTypeSelect
              chooseFileType={chooseFileType}
              setChooseFileType={setChooseFileType}
              placeholder={'Выберете тип'}
              suffixIcon={<SearchOutlined />}
            />
          </FilterContainer>
          <DocumentsMenu />
        </Wrapper>
      </Container>
    </>
  );
};

const FilterContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: 20%;
  height: 40px;
  align-self: flex-start;
`;
const Wrapper = styled.div`
  padding-top: 2%;
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  row-gap: 20px;
`;

const Container = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Title = styled.h1`
  all: unset;
  line-height: 1.3;
  font-weight: 500;
  font-size: 1.5rem;
  display: flex;
  justify-content: flex-start;
  width: 100%;
`;
