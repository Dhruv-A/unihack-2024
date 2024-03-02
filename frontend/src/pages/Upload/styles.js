import styled from "styled-components";

const PageContainer = styled.div`
  padding: 50px;
  height: 100%;
`;

const UploadContainer = styled.div`
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
`;

const UploadWrapper = styled.div`
  height: 300px;
  width: 500px;
  display: flex;
  border: 3px solid #222222;
  border-radius: 10px;
  border-style: dashed;
  padding: 20px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-spacing: 2px;
`;

const Column = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 5rem;
`;

const Translate = styled.button`
  background: #2D261F;
  width: 100%;
  height: 10px;
  padding: 25px;
  border-radius: 10px;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
`;

export default {
  Column,
  PageContainer,
  UploadContainer,
  UploadWrapper,
  Translate
}