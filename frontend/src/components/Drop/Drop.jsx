import S from './styles';
import Dropzone from 'react-dropzone'
import axios from 'axios';

import File from 'assets/upload.svg'
import { useState, useCallback, useEffect } from 'react';
import Progress from 'components/Progress';
import Selection from 'components/Selection';
import UploadedFile from 'components/UploadedFile';

export default function Drop({files, setFiles}) {
  const [mapFiles, setMapFiles] = useState([]);
  const [rejectedfiles, setRejectedFiles] = useState([]);

  const [progress, setProgress] = useState(0);
  const [completed, setCompleted] = useState(false);

  const onDrop = useCallback(async (acceptedFiles, fileRejections) => {
    try {
      if (acceptedFiles?.length) {
        // Set files state
        setFiles(previousFiles => [...previousFiles, ...acceptedFiles]);
      }

      if (fileRejections?.length) {
        // Set rejected files state
        setRejectedFiles(previousFiles => [...previousFiles, ...fileRejections]);
      }
    } catch (error) {
      console.error(`Error handling file`, error);
    }
  }, []);

  const loadProgress = (size) => {
    let current = 0;
    if (progress != 100) {
      for (let i = 0; i < size; i++) {
        const result = Math.floor(((i+1)/size) * 100);
        setProgress(result);
        if(result == 100) {
          console.log('HERE!')
          return result;
        }
      }
    }
    setTimeout(function(){
      setCompleted(true);
    }, 2500); //delay is in milliseconds 
    
  }
  
  return (
    <>
      {files.length <= 0 ? 
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
      :
        <>
          {completed == false ? 
            <>
              {loadProgress(files[0].size) != 100 ?
                 <Progress progress={progress} /> : null
              }
            </>
            :
            <UploadedFile file={files[0]} />
          }
        </>
      }
    </>
  )
}
