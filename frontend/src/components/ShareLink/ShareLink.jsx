import { Link } from 'react-router-dom'
import S from './styles';

const linkStyle = {
  margin: "1rem",
  textDecoration: "underline",
  color: 'blue'
};

const RetryStyle = {
  margin: "1rem",
  textDecoration: "none",
  color: '#FFFFFF'
};


export default function ShareLink({link}) {
  return (
    <S.LinkContainer>
      <h3>Annotate and share are with your friends:</h3>
      <Link style={linkStyle} to={link}>View your generated slides here</Link>
      <S.Retry>
        <Link onClick={() => window.location.reload()} style={RetryStyle}>Convert again?</Link>
      </S.Retry>
    </S.LinkContainer>
  )
}
