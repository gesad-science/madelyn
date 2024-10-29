class TokensFixer:

    @staticmethod
    def fix_tokens(tokens_list : list[dict]):
        tokens = []
        for token in tokens_list:
            if '##' in token['word']:
                word = token['word']
                word = word.replace('#', '')
                tokens[len(tokens)-1]['word'] += word
                tokens[len(tokens)-1]['end'] = token['end']
            else:
                tokens.append(token)
        return tokens