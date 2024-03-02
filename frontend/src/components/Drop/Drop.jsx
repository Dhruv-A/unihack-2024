import S from './styles';
import Dropzone from 'react-dropzone'
import axios from 'axios';

import File from 'assets/upload.svg'
import { useState, useCallback, useEffect } from 'react';

export default function Drop() {
  const [files, setFiles] = useState([]);
  const [mapFiles, setMapFiles] = useState([]);
  const [rejectedfiles, setRejectedFiles] = useState([]);


  useEffect(() => {
    console.log('Added file', files);
  }, [files])

  const onDrop = useCallback(async (acceptedFiles, fileRejections) => {
    try {
      if (acceptedFiles?.length) {
        // Set files state
        setFiles(previousFiles => [...previousFiles, ...acceptedFiles]);
        
        // Handle file upload
        await handleFileUpload(acceptedFiles[0]); // Assuming only one file is uploaded
      }

      if (fileRejections?.length) {
        // Set rejected files state
        setRejectedFiles(previousFiles => [...previousFiles, ...fileRejections]);
      }
    } catch (error) {
      console.error(`Error handling file`, error);
    }
  }, []);

  const handleFileUpload = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://127.0.0.1:5173/translate_slide', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      console.log(response.data);
    } 
    catch (error) {
      console.error(`Error uploading file:`, error);
    }
  }

  return (
    <Dropzone onDrop={onDrop}>
      {({getRootProps, getInputProps}) => (
        <section>
          <div {...getRootProps()}>
            <input {...getInputProps()} />
            <S.FileWrapper>
              <S.File src={File}/>
              <p>Drag and drop a file, or click to select files</p>
            </S.FileWrapper>
          </div>
        </section>
      )}
    </Dropzone>
  )
}
