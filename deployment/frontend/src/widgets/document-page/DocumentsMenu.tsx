import React, { type ReactElement, useEffect, useState } from 'react';
import { DocumentElement } from '@/features/elemet/DocumentElement.tsx';
import styled from 'styled-components';
import { documentData } from '@/shared/data/document.data.ts';
import axios from 'axios';
import { message } from 'antd';
import { IDocumentObject } from '@/shared/interfaces/document.interface.ts';

export const DocumentsMenu = (): ReactElement => {
  const [messageApi, contextHolder] = message.useMessage();
  const [documents, setDocument] = useState<IDocumentObject[]>([]);
  const fetchData = async (isMounted?: boolean): Promise<void> => {
    try {
      const response: IDocumentObject[] = (
        await axios.get(`${import.meta.env.VITE_API_URL}/documents`)
      ).data;
      if (isMounted) {
        setDocument(response);
      }
    } catch (e) {
      messageApi.error(`Ошибка загрузки: ${e}`);
    }
  };

  useEffect(() => {
    let isMounted = true;
    void fetchData(isMounted);
    return (): void => {
      isMounted = false;
    };
  }, []);

  return (
    <Wrapper>
      {contextHolder}
      {documents?.length > 0
        ? documents?.map((elem: IDocumentObject) => (
            <DocumentElement fetchData={fetchData} key={elem.id} elem={elem} />
          ))
        : 'У вас нет документов'}
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
