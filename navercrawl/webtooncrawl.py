import requests
from bs4 import BeautifulSoup
import persistence_01.webtoonDAO as DAO

mDao = DAO.webtoonDAO()

compare_writer = ''
for i in range(1, 6):
    url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=180378&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={}'.format(
        i)
    resp = requests.get(url)

    if resp.status_code != 200:
        print('존재하지 않은 URL')
    else:
        soup = BeautifulSoup(resp.text, 'html.parser')
        reply_list = soup.select('div.score_result li')

        for i, reply in enumerate(reply_list):
            previous_write = reply.select('div dl dt em a span')[0].text.strip()
            cut_index = previous_write.find('(')
            content = reply.select('span#_filtered_ment_{}'.format(i))[0].text.strip()
            score = reply.select('div.star_score em')[0].text.strip()
            reg_date = reply.select('div.score_reple em')[1].text.strip()[11:]

            writer = ''
            if cut_index > 0:
                writer = previous_write[:cut_index]
            else:
                writer = previous_write

            if i == 0:
                if compare_writer != writer:
                    compare_writer = writer
                else:
                    print('Finished Collect:)')

            print('=====================================')
            print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
            print('작성자: ', previous_write)
            print('내용: ', content)
            print('평점: ', score)
            print('시:분: ', reg_date)
            print('=====================================')
            print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')

            data = {'content': content,
                    'writer': writer,
                    'score': score,
                    'reg_data': reg_date}

            mDao.mongo_write(data)