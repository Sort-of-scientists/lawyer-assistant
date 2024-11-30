import React, { type ReactElement, useEffect, useState } from 'react';
import { Button, Input, message, SelectProps } from 'antd';
import styled from 'styled-components';
import { BaseInput } from '@/features/input/BaseInput.tsx';
import { CreateFileModal, ICreateDocument } from '@/features/modal/CreateFileModal.tsx';
import { useNavigate } from 'react-router-dom';
import { DOCUMENTS } from '@/shared/constants/paths.ts';
import { BaseSelect } from '@/features/select/BaseSelect.tsx';
import axios from 'axios';

export const MainPageInfo = (): ReactElement => {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [messageApi, contextHolder] = message.useMessage();

  const [fileType, setFileType] = useState<SelectProps['options']>([]);
  const [chooseFileType, setChooseFileType] = useState<{ value: string }>({ value: 'Загрузка' });

  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      try {
        const response = (await axios.get(`${import.meta.env.VITE_API_URL}/types`)).data;
        if (isMounted) {
          const options = response.map((elem, i) => ({ value: elem }));
          setFileType(options);
          setChooseFileType(options[0]);
        }
      } catch (e) {
        messageApi.error(`Ошибка загрузки: ${e}`);
      }
    };
    void fetchData();
    return () => {
      isMounted = false;
    };
  }, []);
  const handleCancel = () => {
    setOpen(false);
  };

  const showModal = () => {
    if (loading) return;
    setOpen(true);
  };

  const handlerEditOnClick = (value: ICreateDocument): void => {
    setLoading(true);
    const { customFields, ...rest } = value;
    const fields = { ...rest };
    for (const field of customFields) {
      fields[field.name] = field.value;
    }

    const params = {
      n_predict: 100,
      temperature: 0.01,
    };
    const data = { type: chooseFileType.value, fields: { ...fields }, params };
    void (async (): Promise<void> => {
      await axios
        .post(`${import.meta.env.VITE_API_URL}/generate`, data)
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
            <Description>Создайте новый документ по шаблону</Description>
          </TextContainer>
          <SearchContainer>
            <StyledSelect
              options={fileType}
              onSelect={v => setChooseFileType(v)}
              value={chooseFileType}
              placeholder={'Купли-продажи'}
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

const StyledSelect = styled(BaseSelect)`
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
