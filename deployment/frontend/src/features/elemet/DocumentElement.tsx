import React, { type ReactElement, useState } from 'react';
import styled from 'styled-components';
import { DocumentSvg } from '@/shared/svg/document.svg.tsx';
import { Button, theme } from 'antd';
import { IDocumentData } from '@/shared/data/document.data.ts';
import { DeleteOutlined } from '@ant-design/icons';
import { EditFileModal } from '@/features/modal/EditFileModal.tsx';

interface IDocumentElement {
  elem: IDocumentData;
}
export const DocumentElement = ({ elem }: IDocumentElement): ReactElement => {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleCancel = () => {
    setOpen(false);
  };

  const showModal = () => {
    if (loading) return;
    setOpen(true);
  };

  const handlerEditOnClick = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setOpen(false);
    }, 3000);
  };

  return (
    <DocumentWrapper>
      <EditFileModal handleCancel={handleCancel} open={open} handleOk={handlerEditOnClick} />
      <DocumentIconStyles>
        <DocumentSvg />
      </DocumentIconStyles>
      <InfoWrapper>
        <Text>{elem.title}</Text>
        <Description>{elem.description}</Description>
        <ButtonWrapper>
          <StyledButton onClick={showModal} color="default" variant="filled">
            Редактировать
          </StyledButton>
          <SummaryButton defaultHoverColor={'#f5f5f5'} type={'dashed'}>
            Сводка
          </SummaryButton>
        </ButtonWrapper>
      </InfoWrapper>
      <DeleteWrapper>
        <DeleteOutlined />
      </DeleteWrapper>
    </DocumentWrapper>
  );
};

const DocumentWrapper = styled.div`
  position: relative;
  min-width: 600px;
  background: var(--primary1-color);
  width: 100%;
  height: 200px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  border-radius: 10px;
  border: 1px solid var(--border-base-color);
`;

const InfoWrapper = styled.div`
  display: flex;
  width: 90%;
  padding: 5% 5% 5%;
  justify-content: space-between;
  align-items: flex-start;
  flex-direction: column;
  height: 100%;
  row-gap: 20px;
`;

const DocumentIconStyles = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Text = styled.h2`
  all: unset;
  line-height: 1;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: left;
  margin-top: -20px;
`;
const Description = styled.p`
  all: unset;
  line-height: 1.5;
  text-align: left;
`;

const ButtonWrapper = styled.div`
  display: flex;
  flex-direction: row;
  column-gap: 10px;
`;

const StyledButton = styled(Button)``;

const DeleteWrapper = styled.div`
  position: absolute;
  z-index: 1;
  right: 15px;
  top: -40px;
`;

const SummaryButton = styled(Button)`
  &:hover {
    color: var(--secondary-color) !important;
    border-color: var(--secondary-color) !important;
  }
`;
