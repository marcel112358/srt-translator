import argparse
from pathlib import Path
import sys
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import srt

class Translator(object):
    """
    Source: https://github.com/agermanidis/autosub
    Class for translating a sentence from a one language to another.
    """
    def __init__(self, language, api_key, src, dst):
        self.language = language
        self.api_key = api_key
        self.service = build('translate', 'v2', developerKey=self.api_key)
        self.src = src
        self.dst = dst

    def __call__(self, sentencesList):
      for attempt in range(10):
        try:
          if not sentencesList or sentencesList.empty():
            return None

          result = self.service.translations().list(
            source=self.src,
            target=self.dst,
            format='text',
            q=[sentence]
          ).execute()

          if 'translations' in result and result['translations'] and \
            'translatedText' in result['translations'][0]:
            return result['translations'][0]['translatedText']

          return None

        except HttpError:
          print("Retry translation in 5 seconds...")
          time.sleep(5)
          continue


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('--src-lang', required=True)
  parser.add_argument('--dest-lang', required=True)
  parser.add_argument('--api-key', required=True)
  args = parser.parse_args()

  try:
    # Open and read the input file
    inputPath = Path(args.input)

    with open(inputPath) as file:
      contents = file.read()
      subs = list(srt.parse(contents))

    # Create the translator instance
    # Start citation
    # Source: https://github.com/agermanidis/autosub 
    src_language = args.src_lang
    dst_language = args.dest_lang
    google_translate_api_key = args.api_key
    translator = Translator(dst_language, google_translate_api_key,
                            dst=dst_language,
                            src=src_language)
    print("Translating from {0} to {1}: ".format(src_language, dst_language))
    # End citation


    for sub in subs:
      print(sub.content)

      translatedString = translator(sub.content)
      sub.content = translatedString

      print(sub.content)
      print('---')

    # Write subtitle to output file
    f = open(args.output, "w")
    f.write(srt.compose(subs))
    f.close()
  except KeyboardInterrupt:
    return 1
  return 0


if __name__ == '__main__':
    sys.exit(main())
