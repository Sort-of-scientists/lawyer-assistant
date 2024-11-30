import React, { type ReactElement, useState } from 'react';
import { Button, Input } from 'antd';
import styled from 'styled-components';
import { BaseInput } from '@/features/input/BaseInput.tsx';
import { CreateFileModal, ICreateDocument } from '@/features/modal/CreateFileModal.tsx';
import { useNavigate } from 'react-router-dom';
import { DOCUMENTS } from '@/shared/constants/paths.ts';

export const MainPageInfo = (): ReactElement => {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const handleCancel = () => {
    setOpen(false);
  };

  const showModal = () => {
    if (loading) return;
    setOpen(true);
  };

  const handlerEditOnClick = (value: ICreateDocument) => {
    console.log('value', value);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setOpen(false);
      navigate(DOCUMENTS);
    }, 3000);
  };
  return (
    <Wrapper>
      <MainContainer>
        <CreateFileModal handleCancel={handleCancel} open={open} handleOk={handlerEditOnClick} />
        <TextContainer>
          <TitleText>Помощник юриста</TitleText>
          <Description>Создайте новый документ по шаблону</Description>
        </TextContainer>
        <SearchContainer>
          <StyledInput placeholder={'Купли-продажи'} />
          <StyledButton onClick={showModal}>Вперед!</StyledButton>
        </SearchContainer>
      </MainContainer>
    </Wrapper>
  );
};

const Wrapper = styled.div`
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
`;
const MainContainer = styled.div`
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  height: 50%;
  width: 80%;
  margin-top: -5%;
`;

const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
  row-gap: 1px;
`;

const Description = styled.p`
  font-size: 2.3rem;
  color: var(--secondary-color);
  line-height: normal;
  width: 100%;
  white-space: nowrap;
  margin-top: 0;
`;
const TitleText = styled.h1`
  all: unset;
  font-weight: bold;
  font-size: 3rem;
  line-height: normal;
  width: 100%;
  white-space: nowrap;
`;

const SearchContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 35%;
  min-width: 30%;
  max-width: 40%;
  margin-top: -1%;
  gap: 12px;
`;

const StyledInput = styled(BaseInput)`
  height: 40px;
  width: 70%;
  border-radius: 8px;
`;

const StyledButton = styled(Button)`
  height: 40px;
  width: 30%;
  border-radius: 8px;
  background-color: var(--secondary-background-color);
  color: var(--primary-color);
`;
