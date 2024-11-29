import React, { type ReactElement } from 'react';
import { PageTitle } from 'deployment/frontend/src/features/page-title/PageTitle.tsx';
import { DocumentsMenu } from 'deployment/frontend/src/widgets/document-page/DocumentsMenu.tsx';
import styled from 'styled-components';
import { BaseRoundSelect } from 'deployment/frontend/src/features/select/BaseRoundSelect.tsx';
import { SearchOutlined } from '@ant-design/icons';

export const DocumentPage = (): ReactElement => {
  return (
    <>
      <PageTitle>Документы</PageTitle>
      <Container>
        <Wrapper>
          <Title>Ваши документы</Title>
          <FilterContainer>
            <BaseRoundSelect placeholder={'Выберете тип'} suffixIcon={<SearchOutlined />} />
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
  width: 100%;
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
