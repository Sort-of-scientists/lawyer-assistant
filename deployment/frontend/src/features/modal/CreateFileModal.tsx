import React, { type ReactElement } from 'react';
import { Button, Modal } from 'antd';
import { BaseInput } from '@/features/input/BaseInput.tsx';
import styled from 'styled-components';
import { CenteredContent } from '@/app/styles/content/ContentStyle.tsx';
import TextArea from 'antd/es/input/TextArea';

interface IEditFileModal {
  handleOk: () => void;
  handleCancel: () => void;
  open: boolean;
}
export const CreateFileModal = ({ handleOk, handleCancel, open }: IEditFileModal): ReactElement => {
  return (
    <Modal
      open={open}
      title={<TitleWrapper>Создать документ</TitleWrapper>}
      onOk={handleOk}
      onCancel={handleCancel}
      width={400}
      style={{ textAlign: 'center' }}
      footer={[<StyledButton onClick={handleOk}>Подтведить</StyledButton>]}
    >
      <Wrapper>
        <Container>
          <Text>Продавец</Text>
          <BaseInput placeholder={'Имя продавца'} />
          <Text>Покупатель</Text>
          <BaseInput placeholder={'Имя покупателя'} />
          <Text>Цена</Text>
          <BaseInput placeholder={'Стоимость товара'} />
          <Text> Предмет договора</Text>
          <TextArea />
        </Container>
      </Wrapper>
    </Modal>
  );
};

const Text = styled.h1`
  all: unset;
  line-height: 2;
  font-size: 1.1rem;
  text-align: left;
`;

const Container = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  column-gap: 30px;
`;

const Wrapper = styled.div`
  ${CenteredContent};
`;

const StyledButton = styled(Button)`
  width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  background-color: var(--secondary-background-color);
  color: var(--primary-color);
`;

const TitleWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
`;
