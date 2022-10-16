2d cnn 의 코드 올립니다. 

def load_dicom : dicom 파일을 읽는 함수 ( path, size=224 )
  환자id 로 경로를 찾아가며 이미지 사이즈는 default 224 임
  
 def get_all_image_paths : 폴더 안의 모든 이미지 파일 중 학습/판단의 자료로 사용할 이미지의 경로를 반환 하는 함수 (brats21id, image_type, folder='train'): 
  환자 id 로 경로를 찾아가며, 이미지 종류 (FLAIR, T1w, T2w, T1wCE) , train/test 를 입력 받음 default 는 train
  시작 이미지는 전체 이미지의 25% 지점 / 마지막 이미지는 전체 이미지의 75% 지점 / interval 은 전체 이미지가 10장 미민이면 모든 이미지, 10장 이상이면 3장씩 건너뜀
  
 def get_all_images : 환자 아이디로 경로를 지정하여 get_all_image_paths 호출, 환자 아이디로된 경로 내의 이미지들을 load_dicom 을 통해 하나의 리스트로 반환 (brats21id, image_type, folder='train', size=225):
 
 def get_all_data_for_train(image_type): : train 용 이미지 자료 취합용 함수
  
 def get_all_data_for_test(image_type) : test 용 이미지 자료 취합용 함수
 
 def get_all_data_for_val(image_type) : validation용 이미지 자료 취합용 함수
