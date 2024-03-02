import ProgressBar from 'react-animated-progress-bar';

import S from './styles';
import { useEffect, useState } from 'react';

export default function Progress({progress}) {
 
  return (
    <>
      <S.Title>Upload in progress...</S.Title>

      <ProgressBar
        width="400px"
        height="10px"
        rect
        fontColor="gray"
        percentage={`${progress}`}
        rectPadding="1px"
        rectBorderRadius="20px"
        bgColor="#222222"
        trackBorderColor="#222222"
        defColor={{
          fair: '#222222',
          good: '#222222',
          excellent: '#222222',
          poor: '#222222',
        }}
      /> 
   
      
    </>
  )
}
