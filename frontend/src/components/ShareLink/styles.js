import styled from "styled-components";

const LinkContainer = styled.div`
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  gap: 1rem;
`;

const Retry = styled.button`
  background: #222222;
  color: #FFFFFF;
  width: 30%;
  padding: 10px;
  border-radius: 10px;
`;

export default {
  LinkContainer,
  Retry
}