from django.shortcuts import render
from django.views import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class PurePaginationView(View):
    def get(self, request):
        numss = []
        for i in range(40):
            numss.append(i)
        # 获取请求页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 使用Pagination进行分页
        p = Paginator(numss, 5, request=request)
        # nums代表一组5个数据
        nums = p.page(page)
        return render(request, 'pure_pagination.html', {
            'nums': nums,
        })
