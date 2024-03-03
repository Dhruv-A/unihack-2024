import Navbar from 'components/Navbar';
import Drop from 'components/Drop';
import axios from 'axios';
import S from './styles';
import Selection from 'components/Selection';
import { useEffect, useState } from 'react';
import Loading from 'components/Loading';
import Link from 'components/ShareLink';


export default function Upload() {
  const [link, setLink] = useState("");
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState([]);
  const [language, setLanguage] = useState("");

  const handleFileUpload = async (file, language) => {
    setLoading(true);
    const formData = new FormData()
    formData.append('file', file)
    formData.append('language', language)

    try {
      const response = await axios.post('http://127.0.0.1:5173/translate_slide', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((res) => {setLoading(false); setLink(res.data)});
    } 
    catch (error) {
      console.error(`Error uploading file:`, error);
    }
  }

  return (
    <S.PageContainer>
      <Navbar />
      {link ? 
        <Link sharelink={link}/>
        :
        <>
          {loading ?
            <Loading />
            :
            <S.UploadContainer>
              <S.UploadWrapper>
                <Drop files={files} setFiles={setFiles}/>
              </S.UploadWrapper>
              <S.Column>
                <Selection setLanguage={setLanguage}/>
                <S.Translate onClick={() => handleFileUpload(files[0], language)}>Translate</S.Translate>
              </S.Column>
            </S.UploadContainer>
          }
        </>
      }
    </S.PageContainer>
  )
}

