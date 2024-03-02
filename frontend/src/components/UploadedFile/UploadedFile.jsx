import File from 'assets/file.svg';
import S from './styles';

export default function UploadedFile({file}) {
  return (
    <S.File>
      <S.FileImg src={File}/>
      <S.FileContent>
        <h3>{file.name}</h3>
        {`Size: ${file.size} kb`}
      </S.FileContent>
    </S.File>
  )
}
