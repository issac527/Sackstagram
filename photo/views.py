from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .models import Photo
from django.contrib import messages

class PhotoList(ListView):
    model = Photo
    template_name = 'photo_list.html'  # 파일 이름 전체를 지정

class PhotoCreate(CreateView):
    model = Photo

    fields = ['text', 'image']
    template_name = 'photo_create.html'
    # template_name_suffix = '_create' # 뒤에 붙는 이름만 바꿈
    success_url = '/'

    def form_valid(self, form):
        # 입력된 자료가 올바른지 체크
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델 폼
            # form.instance는 model의 객체
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form':form})

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name = 'photo_update.html'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect('/')
        else:
            return super(PhotoUpdate,self).dispatch(request, *args, **kwargs)

    # success_url를 쓰지 않고, models.py에 get_absolute_url() 이용
    # success_url을 지정해주면 get_absolute_url()보다 먼저 적용된다.

class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete,self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name = 'photo_detail.html'