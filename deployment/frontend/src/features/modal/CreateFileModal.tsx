import React, { type ReactElement } from 'react';
import { Button, Form, Modal } from 'antd';
import { BaseInput } from '@/features/input/BaseInput.tsx';
import styled from 'styled-components';
import { CenteredContent } from '@/app/styles/content/ContentStyle.tsx';
import { Formik } from 'formik';
import TextArea from 'antd/es/input/TextArea';

export interface ICreateDocument {
  seller: string;
  buyer: string;
  price: string;
  subject: string;
}

interface IEditFileModal {
  handleOk: (value: ICreateDocument) => void;
  handleCancel: () => void;
  open: boolean;
}
export const CreateFileModal = ({ handleOk, handleCancel, open }: IEditFileModal): ReactElement => {
  const initialValues: ICreateDocument = {
    seller: '',
    buyer: '',
    price: '',
    subject: '',
  };

  const onSubmit = (values, { setSubmitting }) => {
    console.log(JSON.stringify(values, null, 2));
    setSubmitting(false);
    handleOk(values as ICreateDocument);
  };

  return (
    <>
      <Formik initialValues={initialValues} onSubmit={onSubmit}>
        {({
          values,
          errors,
          setSubmitting,
          touched,
          handleChange,
          handleBlur,
          handleSubmit,
          isSubmitting,
        }) => (
          <Modal
            open={open}
            title={<TitleWrapper>Создать документ</TitleWrapper>}
            onCancel={handleCancel}
            width={400}
            style={{ textAlign: 'center' }}
            footer={[
              <StyledButton
                type="submit"
                onClick={() => {
                  onSubmit(values, { setSubmitting });
                }}
                disabled={isSubmitting}
              >
                Подтведить
              </StyledButton>,
            ]}
          >
            <Wrapper>
              <Container>
                <Form onSubmit={handleSubmit}>
                  <Container>
                    <Text>Продавец</Text>
                    <BaseInput
                      type="seller"
                      name="seller"
                      onChange={handleChange}
                      onBlur={handleBlur}
                      placeholder={'Имя продавца'}
                      value={values.seller}
                    />
                    <Text>Покупатель</Text>
                    <BaseInput
                      type="buyer"
                      name="buyer"
                      onChange={handleChange}
                      onBlur={handleBlur}
                      value={values.buyer}
                      placeholder={'Имя покупателя'}
                    />
                    <Text>Цена</Text>
                    <BaseInput
                      type="price"
                      name="price"
                      onChange={handleChange}
                      onBlur={handleBlur}
                      value={values.price}
                      placeholder={'Стоимость товара'}
                    />
                    <Text> Предмет договора</Text>
                    <TextArea
                      type="subject"
                      name="subject"
                      onChange={handleChange}
                      onBlur={handleBlur}
                      value={values.subject}
                      placeholder={'Напишите о своей предметной области'}
                    />
                  </Container>
                </Form>
              </Container>
            </Wrapper>
          </Modal>
        )}
      </Formik>
    </>
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
