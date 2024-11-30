import React, { type ReactElement } from 'react';
import { Button, Form, Modal } from 'antd';
import { BaseInput } from '@/features/input/BaseInput.tsx';
import styled from 'styled-components';
import { Formik, FieldArray } from 'formik';
import TextArea from 'antd/es/input/TextArea';

export interface ICreateDocument {
  seller: string;
  buyer: string;
  price: string;
  subject: string;
  customFields: Array<{ name: string; value: string }>;
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
    customFields: [],
  };

  const validate = (values: ICreateDocument) => {
    const errors: Partial<ICreateDocument> = {};
    if (!values.seller) errors.seller = 'Продавец обязателен';
    if (!values.buyer) errors.buyer = 'Покупатель обязателен';
    if (!values.price) errors.price = 'Цена обязательна';
    if (!values.subject) errors.subject = 'Предмет договора обязателен';
    return errors;
  };

  const onSubmit = (values, { setSubmitting }) => {
    console.log(JSON.stringify(values, null, 2));
    setSubmitting(false);
    handleOk(values as ICreateDocument);
  };

  return (
    <>
      <Formik initialValues={initialValues} validate={validate} onSubmit={onSubmit}>
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
                  handleSubmit();
                }}
                disabled={isSubmitting}
              >
                Подтведить
              </StyledButton>,
            ]}
          >
            <Wrapper>
              <Container>
                <Form>
                  <Text>Продавец</Text>
                  <BaseInput
                    name="seller"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.seller}
                    placeholder="Имя продавца"
                  />
                  <Text>Покупатель</Text>
                  <BaseInput
                    name="buyer"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.buyer}
                    placeholder="Имя покупателя"
                  />
                  <Text>Цена</Text>
                  <BaseInput
                    name="price"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.price}
                    placeholder="Стоимость товара"
                  />
                  <Text>Предмет договора</Text>
                  <TextArea
                    name="subject"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.subject}
                    placeholder="Напишите о своей предметной области"
                  />
                  <Text>Кастомные поля</Text>
                  <FieldArray name="customFields">
                    {({ push, remove }) => (
                      <>
                        {values.customFields.map((field, index) => (
                          <CustomField key={index}>
                            <BaseInput
                              name={`customFields[${index}].name`}
                              placeholder="Название"
                              onChange={handleChange}
                              onBlur={handleBlur}
                              value={field.name}
                            />
                            <BaseInput
                              name={`customFields[${index}].value`}
                              placeholder="Значение"
                              onChange={handleChange}
                              onBlur={handleBlur}
                              value={field.value}
                            />
                            <RemoveButton onClick={() => remove(index)} type="button">
                              Удалить
                            </RemoveButton>
                          </CustomField>
                        ))}
                        <AddButton onClick={() => push({ name: '', value: '' })}>
                          Добавить поле
                        </AddButton>
                      </>
                    )}
                  </FieldArray>
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
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
`;

const Container = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  column-gap: 30px;
`;

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const CustomField = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
`;

const AddButton = styled(Button)`
  width: 100%;
  margin-top: 10px;
`;

const RemoveButton = styled(Button)`
  background-color: var(--error-color);
  color: white;
`;

const StyledButton = styled(Button)`
  width: 100px;
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
