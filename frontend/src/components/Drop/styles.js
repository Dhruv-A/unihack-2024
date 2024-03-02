import styled from "styled-components";

const FileWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const File = styled.img`
  width: 30%;
`;


const Upload = styled.button`
  background: #2D261F;
`;

export default {
  File,
  FileWrapper
}