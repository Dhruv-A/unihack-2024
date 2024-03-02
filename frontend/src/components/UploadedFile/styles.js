import styled from "styled-components";

const FileImg = styled.img`
  width: 10%;
`;

const File = styled.div`
  display: flex;
  gap: 2rem;
  justify-content: center;
`;

const FileContent = styled.div`
  display: flex;
  flex-direction: column;
`;


export default {
  File,
  FileContent,
  FileImg
}