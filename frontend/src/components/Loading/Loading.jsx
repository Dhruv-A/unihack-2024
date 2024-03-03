import S from './styles';

export default function Loading() {
  const ContainerVariants = {
    initial: {
      transition: {
        staggerChildren: 0.2
      }
    },
    animate: {
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const DotVariants = {
    initial: {
      y: "0%"
    },
    animate: {
      y: "100%"
    }
  };
  
  const DotTransition = {
    duration: 0.5,
    repeat: Infinity,
    repeatType: 'reverse',
    ease: "easeInOut"
  };

  return (
    <S.Loading>
      <h3>We're generating a link to your translated slides</h3>
      <S.DotsContainer 
        variants={ContainerVariants} 
        initial="initial"
        animate="animate"
      >
        <S.Dots 
          transition={DotTransition}
          variants={DotVariants}
        />
        <S.Dots 
          transition={DotTransition}
          variants={DotVariants}
        />
        <S.Dots 
          transition={DotTransition}
          variants={DotVariants}
        />
      </S.DotsContainer>
    </S.Loading>
  )
}
