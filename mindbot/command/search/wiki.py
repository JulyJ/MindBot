from wikipedia import exceptions as wiki_exceptions, page as wiki_page

from ..commandbase import SearchCommand


class WikiCommand(SearchCommand):
    name = '/wiki'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                page = wiki_page(self._query)
            except wiki_exceptions.PageError:
                self.send_telegram_message('No such page 😭')
            except wiki_exceptions.WikipediaException:
                self.send_telegram_message('Error while processing request 😭')
            else:
                content = page.content[:512]
                self.send_telegram_message('*{p.title}* \n\n{}...\n\n[Read more at Wikipedia]({p.url})'.format(content, p=page))
        else:
            return self.send_telegram_message('Please specify query')