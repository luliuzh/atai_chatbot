import os
import pickle
import rdflib
import json
import numpy as np

class KnowledgeGraph:
    def __init__(self):
        self.graph = rdflib.Graph()

    def _get_graph_cache(self, graph_path, serialized_path):
        """Cache the RDF graph into a binary file."""
        if os.path.exists(serialized_path):
            print("Loading serialized graph...")
            with open(serialized_path, 'rb') as f:
                self.graph = pickle.load(f)
        else:
            print("Parsing KG file...")
            self.graph.parse(graph_path, format='turtle')  # 或 'xml'、'n3' 等

            with open(serialized_path, 'wb') as f:
                pickle.dump(self.graph, f)
            print(f"Serialized graph saved to {serialized_path}")

    def load_graph(self, graph_path, cache_path=None):
      """Loads the graph, using cache if available."""
      if cache_path is None:
          cache_path = graph_path + ".pickle" # 默认缓存文件名

      self._get_graph_cache(graph_path, cache_path)


# 使用示例：
kg = KnowledgeGraph()

# graph_file = "data/14_graph.nt"  # 替换为你的 RDF 文件路径和正确的扩展名 (例如 .ttl, .rdf, .nt)
# cache_file = "data/14_graph.pickle"  # 缓存文件路径
pickle_file = "data/14_graph.pickle"
# kg.load_graph(graph_file, cache_file) #  加载图，并使用缓存


# 直接加载 pickle 文件
with open("data/14_graph.pickle", "rb") as f:
    graph = pickle.load(f)



# 现在可以使用 kg.graph 进行操作了
# 例如，打印图中所有三元组：
# for s, p, o in kg.graph:
#     print(s, p, o)

class multimedia_handler(KnowledgeGraph):
    def __init__(self, KG, json_path=r"data/images.json"):
        self.KG = KG  # 直接是一个 rdflib.Graph 实例
        
        with open(json_path, 'r') as f:
            self.image_net = json.load(f)   
        self.PANELTY = 0.3
        self.imgs = [i['img'] for i in self.image_net]
        self.ids = [set(i['movie'] + i['cast']) for i in self.image_net]

    def ent_to_id(self, entities):
        """从实体名映射到 ID"""
        ent_dic = {}
        for ent_name in entities:
            query = f'''
            PREFIX ddis: <http://ddis.ch/atai/>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX schema: <http://schema.org/>

            SELECT ?obj WHERE {{
                SERVICE <https://query.wikidata.org/sparql> {{
                    ?sub rdfs:label "{ent_name}"@en.
                    ?sub wdt:P345 ?obj.
                }}
            }} LIMIT 1
            '''.strip()

            ent_dic[ent_name] = []
            # 修改为 self.KG.query
            for row, in self.KG.query(query):
                ent_dic[ent_name].append(str(row))

        # 收集所有的 ID
        tmp = []
        for ent_list in ent_dic.values():
            tmp += ent_list
        return tmp

    def show_img(self, entities):
        """根据输入的实体列表，显示最相关的图片"""
        print('=====================', entities)
        id_lst = self.ent_to_id(entities)
        print('=====================', id_lst)
        
        # 计算每张图片的分数
        score_lst = [
            len(set(id_lst) & single_img) - self.PANELTY * len(single_img)
            for single_img in self.ids
        ]
        
        if not score_lst:  # 如果没有任何分数，则返回一个默认值
            return "No matching image found."

        idx = np.argmax(score_lst)  # 找到分数最高的索引
        print('=====================', len(score_lst), idx)
        
        return f'image:{str(self.imgs[idx].split(".")[0])}'



    



# entities = ["Julia Roberts","Pretty Woman"]
entities = ["Denzel Washington"]
entities = ["Sandra Bullock"]       #Let me know what Sandra Bullock looks like. 
multimedia = multimedia_handler(graph)
print(multimedia.show_img(entities))