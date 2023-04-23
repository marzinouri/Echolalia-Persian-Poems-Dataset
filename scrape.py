import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm


class Preprocessor:
    def remove_urls(self, text):
        url_pattern = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
        return re.sub(url_pattern, '', text)

    def remove_footnote(self, text):
        index = text.find("پانویس ها")
        if index == -1:
            return text
        return text[:index]

    def remove_html_tags(self, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def remove_extra_info(self, text):
        index = text.find("توضیحات بخش")
        if index == -1:
            return text
        return text[:index]

class Echolalia:
    def get_all_poets_links(self, path):
        url = "https://echolalia.ir/poets/"
        response = requests.get(
        url=url,
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        poets = soup.find_all("div", class_= "cat")
        all_links = []
        with open(path, "w") as f:
            for poet in tqdm(poets):
                poet_nationality = poet["data-parent-title"].replace("شاعران", "").strip()
                poet_name = poet["data-title"]
                poet_link_raw = poet.find_all("a", class_="link")
                poet_link = poet_link_raw[0]['href']
                sample = {}    
                sample['poet_nationality'] = poet_nationality
                sample['poet_name'] = poet_name
                sample['poet_link'] = poet_link
                j_sample = json.dumps(sample, ensure_ascii = False)
                f.write(j_sample)
                f.write('\n')
                all_links.append(j_sample)
        return all_links    

    def get_poems_of_poet(self, link):
        page_num = 1
        links = []
        names = []
        while True:
            page_link = link+f'page/{page_num}/'
            response = requests.get(
            url=page_link,
            )
            soup = BeautifulSoup(response.content, 'html.parser')
            posts = soup.find_all("div", class_="posts")
            titles = posts[0].find_all("a", class_="format-bubble")
            if len(titles)==0:
                break
            for title in titles:
                links.append(title['href'])
                names.append(title['title'])
            page_num+=1
        return names, links

    def get_poem_text(self, link):
        page_link = link
        response = requests.get(
            url=page_link,
            )
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find("div", class_="post-content")
        paragraphs = content.find_all("p")
        p_texts = []
        prep = Preprocessor()
        for p in paragraphs:
            refined_p = str(p).replace('<br/>','\n')
            refined_p = prep.remove_html_tags(refined_p)
            refined_p = refined_p.replace("اِکولالیا در اینستاگرام","")
            refined_p = refined_p.replace("ترجمه از","")
            refined_p = refined_p.replace("اکولالیا |","")
            refined_p = re.sub(r'#\w+', '', refined_p)
            refined_p = prep.remove_urls(refined_p)
            p_texts.append(refined_p.strip())
        text = prep.remove_extra_info(prep.remove_footnote(re.sub('\n+', '\n', "\n".join(p_texts)))).strip()
        return text

    def create_dataset(self, input_path, output_path):
        with open(input_path, "r") as f:
            lines = f.readlines()
        poems = []
        for line in tqdm(lines):
            line = line.strip()
            poet_dict = json.loads(line)
            titles, poem_links = self.get_poems_of_poet(poet_dict['poet_link'])
            with open(output_path, "a") as f:
                for index, link in enumerate(poem_links):
                    text = self.get_poem_text(link)
                    sample = {}
                    title = re.sub(r'/.*', '', titles[index])
                    if "شرح زندگی و آثارش" in title:
                        continue
                    sample['title'] = title.strip()
                    sample['link'] = link
                    sample['poem'] = text
                    sample['poet_nationality'] = poet_dict['poet_nationality']
                    sample['poet_name'] = poet_dict['poet_name']
                    sample['poet_link'] = poet_dict['poet_link']
                    j_sample = json.dumps(sample, ensure_ascii = False)
                    poems.append(j_sample)
                    f.write(j_sample)
                    f.write('\n')

echolalia = Echolalia()
path = "links.txt"
echolalia.get_all_poets_links(path)
echolalia.create_dataset(path, "poems.txt")
