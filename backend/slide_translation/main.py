from .find_and_replace import FindAndReplace

if __name__=='__main__':
    slide_translator = FindAndReplace()
    file_name = 'sample_1.pptx'
    slide_translator.replace_text_in_presentation(file_name, 'DE', f'sample_presentations/{file_name}')
