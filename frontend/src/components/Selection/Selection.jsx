import { useEffect, useState } from 'react';
import S from './styles';

const languageOptions = [
  "AR - Arabic",
  "BG - Bulgarian",
  "CS - Czech",
  "DA - Danish",
  "DE - German",
  "EL - Greek",
  "EN-GB - English",
  "ES - Spanish",
  "ET - Estonian",
  "FI - Finnish",
  "FR - French",
  "HU - Hungarian",
  "ID - Indonesian",
  "IT - Italian",
  "JA - Japanese",
  "KO - Korean",
  "LT - Lithuanian",
  "LV - Latvian",
  "NB - Norwegian",
  "NL - Dutch",
  "PL - Polish",
  "PT - Portuguese",
  "RO - Romanian",
  "RU - Russian",
  "SK - Slovak",
  "SL - Slovenian",
  "SV - Swedish",
  "TR - Turkish",
  "UK - Ukrainian",
  "ZH - Chinese"
];

export default function Selection({setLanguage}) {
  return (
    <div>
      <S.Selection onChange={(e) => setLanguage(e.target.value)} defaultValue="" name="target-language">
        <option hidden value="">Select target language</option>
        {languageOptions.map(option => <option value={option.split("-")[0].trim()}>{option}</option>)}
      </S.Selection>
    </div>
  )
}
