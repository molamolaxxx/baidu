class B_item():
    def __init__(self):
        self.is_available=False

        self.id=None
        self.lemmaId=None
        self.title=None
        self.abstract=None
        self.content=None
        self.s_content = None
        self.t_content = None
        self.img=None
        self.last_time=None
        self.ref=None
        self.click=None
        self.share=None
        self.good=None
        self.edit_time=None
        self.tag=None
        self.items=None
        self.flag=None
        #编辑者信息
        self.editor_goodVersionCount=None
        self.editor_commitPassedCount=None
        self.editor_level=None
        self.editor_featuredLemmaCount=None
        self.editor_createPassedCount=None
        self.editor_commitTotalCount=None
        self.editor_experience=None
        self.editor_passRatio=None


if __name__ == '__main__':
    item=B_item()
    print(item.items)
