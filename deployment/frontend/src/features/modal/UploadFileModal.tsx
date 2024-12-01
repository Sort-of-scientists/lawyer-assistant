// import React, { type ReactElement } from 'react';
// import { message, Modal, UploadProps } from 'antd';
// import Dragger from 'antd/es/upload/Dragger';
// import { type RcFile } from 'antd/lib/upload';
// import axios from 'axios';
// import { translit } from '@/shared/utils/utils.ts';
// import { InboxOutlined } from '@ant-design/icons';
//
// export interface IFileWithInfoResponse {
//   content: string;
//   fileId: string;
//   fileName: string;
//   contentType: string;
//   size: number;
// }
// export const uploadFileApi = async (
//   data: string | Blob | RcFile,
// ): Promise<IFileWithInfoResponse | undefined> => {
//   const file = new FormData();
//   if (typeof data !== 'string' && 'name' in data) {
//     const name = translit(data?.name);
//     file.append('originalname', data?.name);
//     file.append('name', name);
//   }
//
//   file.append('file', data);
//   return (
//     await axios.post(`${import.meta.env.VITE_API_URL}/file/up/`, file, {
//       headers: {
//         'Content-Type': 'multipart/form-data;charset=utf-8',
//       },
//     })
//   ).data;
// };
// interface IUploadFileModal {}
// export const UploadFileModal = ({}: IUploadFileModal): ReactElement => {
//   const [messageApi, contextHolder] = message.useMessage();
//   const validFileUpload = (fileType: string): boolean => {
//     return fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
//   };
//
//   const props: any = {
//     name: 'file',
//     multiple: false,
//     beforeUpload: (file: RcFile): boolean => {
//       const isValid = validFileUpload(file.type);
//       if (!isValid) {
//         messageApi.error(`${file.name} is not a valid file`);
//       }
//       return isValid;
//     },
//     onChange(info): void {
//       const { status } = info.file;
//       if (status === 'done') {
//         messageApi.success(`${info.file.name} file uploaded successfully.`);
//       } else if (status === 'error') {
//         messageApi.error(`${info.file.name} file upload failed.`);
//       }
//     },
//     async customRequest({ file, onSuccess, onError }): Promise<void> {
//       if (typeof file === 'string') return;
//       try {
//         void messageApi.loading('Загрузка', 999999);
//         const response = await uploadFileApi(file);
//         if (!response) return;
//         onSuccess?.(response);
//         messageApi.destroy();
//         messageApi.success(
//           'Файл успешно загружен на сервер!\n' +
//             'Перейдите на другую страницу для генерации презентации',
//           10,
//         );
//       } catch (e) {
//         onError?.(e as ProgressEvent);
//         messageApi.error('При загрузке файла произошла ошибка');
//       }
//     },
//   };
//
//   return (
//     <Modal>
//       <Dragger {...props} fileList={[]}>
//         <div>
//           <p className="ant-upload-drag-icon">
//             {contextHolder}
//             <InboxOutlined />
//           </p>
//           <p className="ant-upload-text">Нажмите или перетащите файл в эту область для загрузки</p>
//           <p className="ant-upload-hint">
//             Поддержка загрузки одного или нескольких файлов. Строго запрещено загружать данные
//             компании или другие запрещенные файлы
//           </p>
//         </div>
//       </Dragger>
//     </Modal>
//   );
// };
