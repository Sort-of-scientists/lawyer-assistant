import React, { ReactElement, forwardRef } from 'react';
import { Card as AntCard } from 'antd';
import * as S from 'deployment/frontend/src/features/content/wrapper/content-wrapper.styles.ts';

interface CardProps extends Omit<AntCard, 'className'> {
  className?: string;
  children?: React.ReactNode;
}

export const ContentWrapper = forwardRef<HTMLDivElement, Omit<CardProps, 'className'>>(
  ({ children }, ref): ReactElement => {
    return <S.Wrapper ref={ref}>{children}</S.Wrapper>;
  },
);
