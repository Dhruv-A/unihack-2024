import {motion} from 'framer-motion';
import styled from 'styled-components';

const Loading = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5rem;
  align-items: center;
  justify-content: center;
  height: 80%;
`;

const Dots = styled(motion.span)`
  display: block;
  width: 2rem;
  height: 2rem;
  background-color: #222222;
  border-radius: 50%;
`;

const DotsContainer = styled(motion.div)`
  width: 10rem;
  height: 5rem;
  display: flex;
  justify-content: space-around;
`;

export default {
  Dots,
  DotsContainer,
  Loading
}