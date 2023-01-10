from typing import List


class TreeStore:
    
    def __init__(self, obj_list :List[dict]):
        self._obj_list = obj_list
        self._items_ids = {}
        self._items_children_items = {}
        self._create_indexes(obj_list)
        
    def _create_indexes(self, obj_list :List[dict]) -> None:
        """ Индексирования списка """
        
        self._items_ids = {item["id"]:index for index, item in enumerate(obj_list)}
        for item in obj_list:
            if item["parent"] == "root":
                self._items_children_items[item["id"]] = set()
                continue
            parent_item_id :int = self._obj_list[self._items_ids[item["parent"]]]["id"]
            self._items_children_items[parent_item_id] :set = self._items_children_items \
                                                                .get(parent_item_id, set())
            self._items_children_items[parent_item_id].add(item["id"])
            
            """
            Пояснение к выбору типа для хранения id:
            Выбрал set исходя из того, что при удалении в худшех случаях у массива будет O(n), а у set O(1).
            Также при добавлении в конец массива количество операций O(1),
            но  можент увеличиться в случае выделения доп.памяти, а у set O(1) всегда.
            Но это без учета возможных коллизий в set
            """
        
    def get_all(self) -> List[dict]:
        """ Получение всех элементов списка """
        
        return self._obj_list
    
    def get_item(self, id :int) -> dict:
        """ Получение элемента по id """
        try:
            return self._obj_list[self._items_ids[id]]
        except KeyError:
            return None

    def get_children(self, id :int) -> List[dict]:
        """ Получение дочерних элементов элемента по переданному id """
        
        children_item_ids = self._items_children_items.get(id)
        if not children_item_ids:
            return []
        return [self.get_item(id) for id in children_item_ids]
    
    def get_all_parents(self, id :int) -> List[dict]:
        """ Выборка всех родителей переданного id элемента """
        
        item :dict = self.get_item(id)
        if not item:
            return []
        parent_items :List[dict] = []
        while item["parent"]!="root":
            item :dict = self.get_item(item["parent"])
            parent_items.append(item)
        return parent_items
            


items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]

ts = TreeStore(items)
print(ts.get_all())
print(ts.get_item(7))
print(ts.get_children(4))
print(ts.get_all_parents(7))
