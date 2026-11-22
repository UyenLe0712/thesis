import shutil, os
p = "/content/drive/MyDrive/thesis/colab_kaggle/luoi-test-c-dpo/s1_merged"
if os.path.isdir(p): shutil.rmtree(p); print("da xoa", p)
else: print("khong co", p)
