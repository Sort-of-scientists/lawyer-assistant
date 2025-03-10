import React, { type ReactElement, useEffect, useState } from 'react';
import { Button, Input, message, SelectProps } from 'antd';
import styled from 'styled-components';
import { BaseInput } from '@/features/input/BaseInput.tsx';
import { CreateFileModal, ICreateDocument } from '@/features/modal/CreateFileModal.tsx';
import { useNavigate } from 'react-router-dom';
import { DOCUMENTS } from '@/shared/constants/paths.ts';
import { BaseSelect } from '@/features/select/BaseSelect.tsx';
import axios from 'axios';
import {
  DocumentTypeSelect,
  IChooseFileType,
} from '@/widgets/document-type/DocumentTypeSelect.tsx';
import { api } from '@/path.ts';

export const MainPageInfo = (): ReactElement => {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [messageApi, contextHolder] = message.useMessage();

  const [chooseFileType, setChooseFileType] = useState<IChooseFileType>({ value: 'Загрузка' });

  const handleCancel = () => {
    setOpen(false);
  };

  const showModal = () => {
    if (loading) return;
    setOpen(true);
  };

  useEffect(() => {
    if (loading) {
      void messageApi.loading({ content: 'Генерация файла', duration: 9000 });
    }
  }, [loading]);
  const handlerEditOnClick = (value: ICreateDocument): void => {
    setLoading(true);
    const { customFields, ...rest } = value;
    const fields = { ...rest };
    for (const field of customFields) {
      fields[field.name] = field.value;
    }

    const params = {
      n_predict: 2000,
      temperature: 0.01,
    };
    const data = { type: chooseFileType.value, fields: { ...fields }, params };
    void (async (): Promise<void> => {
      await axios
        .post(`${api}/generate`, data)
        .then(() => navigate(DOCUMENTS))
        .catch(e => messageApi.error(`Ошибка создания файла: ${e}`));
    })();
  };

  return (
    <>
      {contextHolder}
      <Wrapper>
        <MainContainer>
          <CreateFileModal handleCancel={handleCancel} open={open} handleOk={handlerEditOnClick} />
          <TextContainer>
            <TitleText>Помощник юриста</TitleText>
            <Description>Сгенерируйте документ с помощью нейронной сети</Description>
          </TextContainer>
          <SearchContainer>
            <StyledSelect
              chooseFileType={chooseFileType}
              setChooseFileType={setChooseFileType}
              placeholder={'Купли-продажи'}
              defaultSelection={true}
            />
            <StyledButton onClick={showModal}>Вперед!</StyledButton>
          </SearchContainer>
        </MainContainer>
      </Wrapper>
    </>
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

const StyledSelect = styled(DocumentTypeSelect)`
  width: 80%;
  height: 40px;
`;

const StyledButton = styled(Button)`
  height: 40px;
  width: 30%;
  border-radius: 8px;
  background-color: var(--secondary-background-color);
  color: var(--primary-color);
`;
