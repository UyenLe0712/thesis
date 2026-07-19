# DỮ LIỆU THẬT — để trình & xin thầy DUYỆT 3 dataset

> **Tài liệu này để làm gì?** Cho thầy thấy 3 bộ dữ liệu mình dùng *trông thật sự ra sao*. Mỗi bộ trình bày 3 phần: **(1) là gì → (2) một mẫu (item) gồm những gì → (3) ba mẫu thật + giải thích dễ hiểu**.
> Mọi ảnh và đoạn JSON đều **lấy thẳng từ dataset đã tải về máy** (`dataset_samples/`), đã được kiểm tra đối chiếu với nguồn HuggingFace — **khớp 100%, không chỉnh, không tự bịa**. Phần *Giải thích* do mình viết cho dễ hiểu, **chỉ nói đúng những gì có trong dữ liệu**.

## Một số từ sẽ gặp (đọc 1 lần cho quen)

| Từ | Nói nôm na |
|--|--|
| **View-hierarchy** | Bảng kèm theo mỗi ảnh, liệt kê **mọi nút/ô trên màn** và **toạ độ (nằm ở đâu)** của chúng. Như “bản đồ các nút”. |
| **bounds (khung)** | 4 con số `[[x1,y1],[x2,y2]]` = hình chữ nhật bao quanh một nút = **vị trí thật** của nút. |
| **Grounding** | Kiểm máy có **chỉ đúng nút** không: điểm máy định bấm có nằm TRONG khung của nút cần bấm không. |
| **Hallucination (bịa)** | Máy nhắc tới một nút **không hề có** trên màn. |
| **Episode (quy trình)** | Một chuỗi thao tác để làm xong 1 việc (vd: mở app → bấm → gõ → xong). |
| **Gold trajectory (thứ tự đúng)** | Chuỗi thao tác đúng từng bước **có sẵn** trong dataset → cho biết **bước nào trước bước nào**. |
| **Kendall τ-b** | Điểm đo **hai thứ tự giống nhau bao nhiêu**: −1 (ngược hẳn) → 0 (lung tung) → +1 (giống y). |

---

# DATASET 1 — MobileViews

## 1. MobileViews là gì?

Là **kho ~600.000 ảnh chụp màn hình ứng dụng Android**. Điều đặc biệt: **mỗi ảnh đi kèm một “view-hierarchy”** — một bảng do điện thoại tự xuất ra, ghi lại **mọi nút/ô trên màn đó + toạ độ chính xác** của chúng. Nói nôm na: không chỉ có *ảnh*, mà còn có cả *“bản đồ các nút”* của ảnh.

> **Vì sao em cần bộ này:** nhờ biết **vị trí thật của từng nút**, khi AI viết hướng dẫn “bấm nút X”, em **đối chiếu được** AI có chỉ đúng chỗ không (grounding) và có bịa nút không (hallucination) — mà **KHÔNG cần ai soạn sẵn bài hướng dẫn mẫu**. → đây là dữ liệu cho **nhánh 1 ảnh**.
> *(Lưu ý: MobileViews là bản thảo chưa bình duyệt (preprint) → em chỉ dùng nó làm **nguồn ảnh + nhãn vị trí**, không dùng làm cơ sở lý thuyết.)*

## 2. Một mẫu (item) MobileViews gồm những gì?

Một item = **1 màn hình**, gồm 3 file đi cùng nhau: **ảnh** (`.jpg`) · **view-hierarchy** (`.viewhierarchy.json` — bảng các nút) · **bản XML gốc** của Android (`.uiautomator.xml`).

Ví dụ mở thử file view-hierarchy của 1 màn, nó ghi như sau (mỗi dòng là 1 nút/ô):

![MobileViews item 1](../dataset_samples/mobileviews/item1_state39.jpg)

**Vài thông tin chung của màn (lấy nguyên từ file):**

```
app đang mở = com.xero.projects/.ui.feature.modifytimeentry.activities.ModifyTimeEntryActivity
kích thước (pixel) = 2340 x 1080
tổng số phần tử trên màn = 25
```

**Toàn bộ 25 phần tử của màn này** — cột `bounds` chính là VỊ TRÍ (toạ độ) của nút (✓ = có tính chất đó):

| # | text (chữ) | mô tả | loại (class) | bounds (vị trí) | bấm? | nhập? | resource_id |
|--|--|--|--|--|--|--|--|
| 0 |  |  | FrameLayout | [[60,480],[1020,1368]] |  |  |  |
| 1 |  |  | LinearLayout | [[108,528],[972,1320]] |  |  |  |
| 2 |  |  | FrameLayout | [[108,528],[972,1320]] |  |  | content |
| 3 |  |  | LinearLayout | [[108,528],[972,1320]] |  |  | parentPanel |
| 4 |  |  | FrameLayout | [[108,528],[972,1320]] |  |  | customPanel |
| 5 |  |  | FrameLayout | [[108,528],[972,1320]] |  |  | custom |
| 6 |  |  | TimePicker | [[108,528],[972,1320]] |  |  | timePicker |
| 7 |  |  | LinearLayout | [[108,528],[972,1320]] |  |  |  |
| 8 | Set time |  | TextView | [[108,528],[972,768]] |  |  | input_header |
| 9 |  |  | RelativeLayout | [[108,768],[972,1152]] |  |  | input_mode |
| 10 | Type in time |  | TextView | [[180,846],[442,911]] |  |  | top_label |
| 11 |  |  | RelativeLayout | [[180,935],[500,1152]] |  |  | input_block |
| 12 | 8 |  | EditText | [[180,935],[330,1095]] | ✓ | ✓ | input_hour |
| 13 | : |  | TextView | [[313,965],[330,1062]] |  |  | input_separator |
| 14 | 35 |  | EditText | [[330,935],[480,1095]] | ✓ | ✓ | input_minute |
| 15 | hour |  | TextView | [[180,1095],[264,1152]] |  |  | label_hour |
| 16 | minute |  | TextView | [[330,1095],[459,1152]] |  |  | label_minute |
| 17 |  |  | Spinner | [[635,952],[900,1096]] | ✓ |  | am_pm_spinner |
| 18 | PM |  | CheckedTextView | [[635,952],[756,1096]] |  |  | text1 |
| 19 |  |  | LinearLayout | [[108,1152],[972,1320]] |  |  |  |
| 20 |  | Switch to clock mo… | ImageButton | [[144,1164],[288,1308]] | ✓ |  | toggle_mode |
| 21 |  |  | ScrollView | [[372,1152],[972,1320]] |  |  | buttonPanel |
| 22 |  |  | LinearLayout | [[372,1152],[972,1320]] |  |  |  |
| 23 | Cancel |  | Button | [[408,1164],[672,1308]] | ✓ |  | button2 |
| 24 | OK |  | Button | [[672,1164],[936,1308]] | ✓ |  | button1 |

**Cùng dữ liệu đó ở dạng JSON gốc** (trích 2 phần tử đầu trong bảng `views`, để thầy thấy đúng định dạng thật):

```json
[
  {
    "package": "com.xero.projects",
    "visible": true,
    "checkable": false,
    "child_count": 1,
    "editable": false,
    "clickable": false,
    "is_password": false,
    "focusable": false,
    "enabled": true,
    "content_description": null,
    "children": [
      1
    ],
    "focused": false,
    "bounds": [
      [
        60,
        480
      ],
      [
        1020,
        1368
      ]
    ],
    "resource_id": null,
    "checked": false,
    "text": null,
    "class": "android.widget.FrameLayout",
    "scrollable": false,
    "selected": false,
    "long_clickable": false,
    "parent": -1,
    "temp_id": 0,
    "size": "960*888",
    "signature": "[class]android.widget.FrameLayout[resource_id]None[text]None[enabled,,]",
    "view_str": "3ecafe14aa813f44109e73b198832d61",
    "bound_box": "60,480,1020,1368",
    "content_free_signature": "[class]android.widget.FrameLayout[resource_id]None"
  },
  {
    "package": "com.xero.projects",
    "visible": true,
    "checkable": false,
    "child_count": 1,
    "editable": false,
    "clickable": false,
    "is_password": false,
    "focusable": false,
    "enabled": true,
    "content_description": null,
    "children": [
      2
    ],
    "focused": false,
    "bounds": [
      [
        108,
        528
      ],
      [
        972,
        1320
      ]
    ],
    "resource_id": null,
    "checked": false,
    "text": null,
    "class": "android.widget.LinearLayout",
    "scrollable": false,
    "selected": false,
    "long_clickable": false,
    "parent": 0,
    "temp_id": 1,
    "size": "864*792",
    "signature": "[class]android.widget.LinearLayout[resource_id]None[text]None[enabled,,]",
    "view_str": "0efc82be15532bf12aa2412d4b57838e",
    "bound_box": "108,528,972,1320",
    "content_free_signature": "[class]android.widget.LinearLayout[resource_id]None"
  }
]
```

---

## 3. Ba mẫu thật + giải thích

> **Cách đọc mỗi ví dụ:** nhìn ẢNH (màn hình thật) → **ô viền đỏ** là vị trí thật của một nút mà mình vẽ lại từ view-hierarchy, để thấy *dataset biết chính xác nút nằm đâu*.
> *(Lưu ý: gói tải về là trace của 1 app (Xero Projects) nên 3 ví dụ là 3 màn KHÁC NHAU của cùng app; cả bộ 600.000 màn thì trải nhiều app.)*

### Ví dụ 1

![MobileViews ví dụ 1](../dataset_samples/mobileviews/item1_state39.jpg)

**Dữ liệu thật (tóm tắt — đầy đủ ở `dataset_samples/mobileviews/item1_state39.viewhierarchy.json`):** app `com.xero.projects`, màn *.ui.feature.modifytimeentry.activities.ModifyTimeEntry*, **25 phần tử**; **2 ô nhập** (`8`, `35`); **4 nút bấm** (“Spinner”, “Switch to clock mo…”, “Cancel”, “OK”).

**Giải thích (dễ hiểu):** Ảnh trên là **một màn thật** của ứng dụng *com.xero.projects* (chức năng *.ui.feature.modifytimeentry.activities.ModifyTimeEntry*). Kèm ảnh, dataset cho một bảng liệt kê **25 thành phần** trên màn — mỗi thành phần ghi rõ *là nút hay ô nhập, chữ gì, nằm ở toạ độ nào*. Màn này có **2 ô để gõ chữ** và **4 nút bấm**. **Ô viền đỏ** là mình vẽ lại đúng toạ độ của MỘT nút (lấy từ bảng) — để thầy thấy *dataset biết CHÍNH XÁC nút nằm chỗ nào*. **Vì sao điều này quan trọng:** khi AI của em viết “bấm nút …”, em so điểm AI định bấm với khung thật của nút → **trúng khung = đúng (grounding)**; còn nếu AI nhắc một nút *không có* trong bảng → là **bịa (hallucination)**. Nhờ có sẵn vị trí thật, em chấm được mà **không cần bài hướng dẫn mẫu của người**.

---

### Ví dụ 2

![MobileViews ví dụ 2](../dataset_samples/mobileviews/item2_state203.jpg)

**Dữ liệu thật (tóm tắt — đầy đủ ở `dataset_samples/mobileviews/item2_state203.viewhierarchy.json`):** app `com.xero.projects`, màn *.ui.feature.modifycontact.activities.ModifyContact*, **32 phần tử**; **4 ô nhập** (`dummy_user_input`, `Email address`, `First name`, `Last name`); **3 nút bấm** (“Navigate up (icon)”, “Submit (icon)”, “LinearLayout”).

**Giải thích (dễ hiểu):** Ảnh trên là **một màn thật** của ứng dụng *com.xero.projects* (chức năng *.ui.feature.modifycontact.activities.ModifyContact*). Kèm ảnh, dataset cho một bảng liệt kê **32 thành phần** trên màn — mỗi thành phần ghi rõ *là nút hay ô nhập, chữ gì, nằm ở toạ độ nào*. Màn này có **4 ô để gõ chữ** và **3 nút bấm**. **Ô viền đỏ** là mình vẽ lại đúng toạ độ của MỘT nút (lấy từ bảng) — để thầy thấy *dataset biết CHÍNH XÁC nút nằm chỗ nào*. **Vì sao điều này quan trọng:** khi AI của em viết “bấm nút …”, em so điểm AI định bấm với khung thật của nút → **trúng khung = đúng (grounding)**; còn nếu AI nhắc một nút *không có* trong bảng → là **bịa (hallucination)**. Nhờ có sẵn vị trí thật, em chấm được mà **không cần bài hướng dẫn mẫu của người**.

---

### Ví dụ 3

![MobileViews ví dụ 3](../dataset_samples/mobileviews/item3_state129.jpg)

**Dữ liệu thật (tóm tắt — đầy đủ ở `dataset_samples/mobileviews/item3_state129.viewhierarchy.json`):** app `com.xero.projects`, màn *.ui.feature.modifytask.activities.ModifyTask*, **36 phần tử**; **3 ô nhập** (`Find or create a t…`, `Estimated hours`, `Charge`); **4 nút bấm** (“Navigate up (icon)”, “Submit (icon)”, “Hourly rate”, “SAVE & ADD ANOTHER”).

**Giải thích (dễ hiểu):** Ảnh trên là **một màn thật** của ứng dụng *com.xero.projects* (chức năng *.ui.feature.modifytask.activities.ModifyTask*). Kèm ảnh, dataset cho một bảng liệt kê **36 thành phần** trên màn — mỗi thành phần ghi rõ *là nút hay ô nhập, chữ gì, nằm ở toạ độ nào*. Màn này có **3 ô để gõ chữ** và **4 nút bấm**. **Ô viền đỏ** là mình vẽ lại đúng toạ độ của MỘT nút (lấy từ bảng) — để thầy thấy *dataset biết CHÍNH XÁC nút nằm chỗ nào*. **Vì sao điều này quan trọng:** khi AI của em viết “bấm nút …”, em so điểm AI định bấm với khung thật của nút → **trúng khung = đúng (grounding)**; còn nếu AI nhắc một nút *không có* trong bảng → là **bịa (hallucination)**. Nhờ có sẵn vị trí thật, em chấm được mà **không cần bài hướng dẫn mẫu của người**.

---

# DATASET 2 — AndroidControl

## 1. AndroidControl là gì?

Là bộ **15.283 “quy trình” thao tác thật** (gọi là *episode*) do người thật làm trên **833 ứng dụng**, trung bình ~5,5 bước mỗi quy trình. Mỗi quy trình có một **mục tiêu** (vd “sửa tên một ghi chú”) và **chuỗi thao tác ĐÚNG từng bước** được ghi sẵn — tức là **đã biết bước nào làm trước bước nào**.

> **Vì sao em cần bộ này:** vì có sẵn **thứ tự đúng**, em có thể **xáo trộn** các màn của một quy trình rồi xem **AI có sắp lại đúng thứ tự không** — đó là cách đo *AI có hiểu trình tự thao tác không* (**nhánh nhiều ảnh**). Bộ này **đã được bình duyệt (hội nghị NeurIPS 2024)**.

## 2. Một mẫu (item) AndroidControl gồm những gì?

Một item = **1 quy trình**, gồm: **mục tiêu** + **các bước**. Mỗi bước có: **ảnh màn lúc đó** (`.png`) · **thao tác đúng** cần làm (bấm toạ độ nào / gõ chữ gì / mở app…) · app đang mở. **Bước cuối luôn là “status”** = đánh dấu đã xong việc.

**Các loại thao tác hợp lệ (lấy từ dataset):** `click · long_press · input_text · scroll · navigate_home · navigate_back · open_app · wait · status`.

Mở thử file của 1 quy trình (episode #7057), nó ghi nguyên như sau:

```json
{
  "episode_id": 7057,
  "goal": "I forgot that I already have a note named Grocery in the Keep Notes app, so I want to edit the title of this note from Grocery to Grocery Store Lidl.",
  "num_steps": 3,
  "steps": [
    {
      "step_id": 0,
      "np": 0,
      "active_application": "Keep Notes",
      "previous_actions": "",
      "gold_action": "!FUNCTIONCALL{\"name\": \"click\", \"parameters\": {\"x\": 275, \"y\": 401}}",
      "screen_w": 1080,
      "screen_h": 2400,
      "uid": "427fd821-73a1-4727-9417-611ac26cd91c",
      "screenshot_file": "ep1_7057_step1.png"
    },
    {
      "step_id": 1,
      "np": 1,
      "active_application": "Popup Window",
      "previous_actions": "{\"name\": \"click\", \"parameters\": {\"x\": 275, \"y\": 401}}",
      "gold_action": "!FUNCTIONCALL{\"name\": \"input_text\", \"parameters\": {\"text\": \"Grocery Store Lidl\"}}",
      "screen_w": 1080,
      "screen_h": 2400,
      "uid": "0001df0d-c9ad-4c32-b0d6-80756ab4ccf9",
      "screenshot_file": "ep1_7057_step2.png"
    },
    {
      "step_id": 2,
      "np": 2,
      "active_application": "Keep Notes",
      "previous_actions": "{\"name\": \"click\", \"parameters\": {\"x\": 275, \"y\": 401}}\n{\"name\": \"input_text\", \"parameters\": {\"text\": \"Grocery Store Lidl\"}}",
      "gold_action": "!FUNCTIONCALL{\"name\": \"status\", \"parameters\": {\"goal_status\": \"successful\"}}",
      "screen_w": 1080,
      "screen_h": 2400,
      "uid": "79b18a19-70ad-4743-b582-705efdb4fcad",
      "screenshot_file": "ep1_7057_step3.png"
    }
  ]
}
```

---

## 3. Ba mẫu thật + giải thích

> **Cách đọc:** các ảnh xếp từ TRÁI sang PHẢI = thứ tự đúng của các bước (số 1, 2, 3…). Dưới phần giải thích có liệt kê *thao tác đúng* ở mỗi bước.
> *Ba ví dụ có độ dài khác nhau (3 / 5 / 9 bước) để thấy quy trình ngắn → dài.*

### Ví dụ 1 (quy trình #7057 — 3 bước)

![ep1 b1](../dataset_samples/androidcontrol/ep1_7057_step1.png) ![ep1 b2](../dataset_samples/androidcontrol/ep1_7057_step2.png) ![ep1 b3](../dataset_samples/androidcontrol/ep1_7057_step3.png)

**Mục tiêu (lấy nguyên từ dataset):** “I forgot that I already have a note named Grocery in the Keep Notes app, so I want to edit the title of this note from Grocery to Grocery Store Lidl.”

**Thứ tự đúng (gold) — các thao tác:** **bước 1** bấm vào màn tại điểm (275, 401); **bước 2** gõ chữ “Grocery Store Lidl”; **bước 3** báo ĐÃ XONG việc (bước kết thúc).

**Giải thích (dễ hiểu):** Đây là **một quy trình thật 3 bước** mà người dùng đã làm để hoàn thành mục tiêu trên, trong app **Keep Notes, Popup Window**. Dataset lưu ở MỖI bước: *ảnh màn lúc đó* + *thao tác đúng cần làm*. Đọc các thao tác theo thứ tự (ở trên) là thấy rõ **bước nào phải làm trước bước nào** → đó chính là **THỨ TỰ ĐÚNG**. **Cách em dùng để trình thầy:** em lấy 3 ảnh này, **xáo trộn (giấu thứ tự)**, rồi đưa cho AI và yêu cầu *sắp lại cho đúng*; sau đó so kết quả AI sắp với thứ tự đúng ở trên → ra điểm **Kendall τ-b** (càng gần +1 càng đúng). Đây là cách đo *AI có hiểu trình tự thao tác trong app hay không*. (Bước cuối “status” chỉ là đánh dấu đã xong.)

---

### Ví dụ 2 (quy trình #14851 — 5 bước)

![ep2 b1](../dataset_samples/androidcontrol/ep2_14851_step1.png) ![ep2 b2](../dataset_samples/androidcontrol/ep2_14851_step2.png) ![ep2 b3](../dataset_samples/androidcontrol/ep2_14851_step3.png) ![ep2 b4](../dataset_samples/androidcontrol/ep2_14851_step4.png) ![ep2 b5](../dataset_samples/androidcontrol/ep2_14851_step5.png)

**Mục tiêu (lấy nguyên từ dataset):** “Create a shortcut for me of The Queen's Gambit pdf file to the home screen on the Drive app.”

**Thứ tự đúng (gold) — các thao tác:** **bước 1** bấm vào màn tại điểm (1016, 866); **bước 2** cuộn màn down; **bước 3** bấm vào màn tại điểm (602, 2105); **bước 4** bấm vào màn tại điểm (821, 2252); **bước 5** báo ĐÃ XONG việc (bước kết thúc).

**Giải thích (dễ hiểu):** Đây là **một quy trình thật 5 bước** mà người dùng đã làm để hoàn thành mục tiêu trên, trong app **Drive, Pixel Launcher**. Dataset lưu ở MỖI bước: *ảnh màn lúc đó* + *thao tác đúng cần làm*. Đọc các thao tác theo thứ tự (ở trên) là thấy rõ **bước nào phải làm trước bước nào** → đó chính là **THỨ TỰ ĐÚNG**. **Cách em dùng để trình thầy:** em lấy 5 ảnh này, **xáo trộn (giấu thứ tự)**, rồi đưa cho AI và yêu cầu *sắp lại cho đúng*; sau đó so kết quả AI sắp với thứ tự đúng ở trên → ra điểm **Kendall τ-b** (càng gần +1 càng đúng). Đây là cách đo *AI có hiểu trình tự thao tác trong app hay không*. (Bước cuối “status” chỉ là đánh dấu đã xong.)

---

### Ví dụ 3 (quy trình #3648 — 9 bước)

![ep3 b1](../dataset_samples/androidcontrol/ep3_3648_step1.png) ![ep3 b2](../dataset_samples/androidcontrol/ep3_3648_step2.png) ![ep3 b3](../dataset_samples/androidcontrol/ep3_3648_step3.png) ![ep3 b4](../dataset_samples/androidcontrol/ep3_3648_step4.png) ![ep3 b5](../dataset_samples/androidcontrol/ep3_3648_step5.png) ![ep3 b6](../dataset_samples/androidcontrol/ep3_3648_step6.png) ![ep3 b7](../dataset_samples/androidcontrol/ep3_3648_step7.png) ![ep3 b8](../dataset_samples/androidcontrol/ep3_3648_step8.png) ![ep3 b9](../dataset_samples/androidcontrol/ep3_3648_step9.png)

**Mục tiêu (lấy nguyên từ dataset):** “I want to rename a file related to my photo.”

**Thứ tự đúng (gold) — các thao tác:** **bước 1** cuộn màn down; **bước 2** cuộn màn down; **bước 3** cuộn màn down; **bước 4** bấm vào màn tại điểm (448, 1877); **bước 5** bấm vào màn tại điểm (602, 2129); **bước 6** gõ chữ “Photo”; **bước 7** bấm vào màn tại điểm (875, 956); **bước 8** chờ màn tải xong; **bước 9** báo ĐÃ XONG việc (bước kết thúc).

**Giải thích (dễ hiểu):** Đây là **một quy trình thật 9 bước** mà người dùng đã làm để hoàn thành mục tiêu trên, trong app **Drive**. Dataset lưu ở MỖI bước: *ảnh màn lúc đó* + *thao tác đúng cần làm*. Đọc các thao tác theo thứ tự (ở trên) là thấy rõ **bước nào phải làm trước bước nào** → đó chính là **THỨ TỰ ĐÚNG**. **Cách em dùng để trình thầy:** em lấy 9 ảnh này, **xáo trộn (giấu thứ tự)**, rồi đưa cho AI và yêu cầu *sắp lại cho đúng*; sau đó so kết quả AI sắp với thứ tự đúng ở trên → ra điểm **Kendall τ-b** (càng gần +1 càng đúng). Đây là cách đo *AI có hiểu trình tự thao tác trong app hay không*. (Bước cuối “status” chỉ là đánh dấu đã xong.)

---

# DATASET 3 — ScreenSpot

## 1. ScreenSpot là gì?

Là bộ **~1.272 mẫu** kiểm khả năng “chỉ đúng nút” trên **3 nền tảng: điện thoại / máy tính / web**. Mỗi mẫu rất gọn: **1 ảnh + 1 câu lệnh ngắn** (vd “đóng cửa sổ”) + **đánh dấu sẵn ô chứa nút đúng** cần bấm.

> **Vì sao em cần bộ này:** đây là **“thước chuẩn” đã được giới khoa học công nhận** (bình duyệt) để KIỂM xem *cái máy chấm-vị-trí của em chính xác bao nhiêu %*. Nó giúp **bù độ tin** cho MobileViews (vốn là bản thảo chưa bình duyệt). *(Bộ này chỉ kiểm “bấm 1 nút”, nên chỉ dùng làm đối chứng, không thay nhánh nhiều ảnh.)*

## 2. Một mẫu (item) ScreenSpot gồm những gì?

Một item = **1 ảnh** + các trường: `instruction` (câu lệnh) · `bbox` (ô vị trí đúng, ghi cả dạng 0–1 và pixel) · `data_type` (icon hay chữ) · `data_source` (nền tảng) · `image_size`.

Mở thử file của 1 mẫu, nó ghi nguyên như sau:

![ScreenSpot item 1](../dataset_samples/screenspot/item1.png)

```json
{
  "file_name": "mobile_907cb7d2-9953-476e-b589-5526587c3913.png",
  "platform": "mobile",
  "instruction": "invert the lens",
  "data_type": "icon",
  "data_source": "ios",
  "bbox_normalized_[x1,y1,x2,y2]": [
    0.8247863247863247,
    0.8313586097946287,
    0.9487179487179487,
    0.891785150078989
  ],
  "bbox_pixel_[x1,y1,x2,y2]": [
    965,
    2105,
    1110,
    2258
  ],
  "image_size_[w,h]": [
    1170,
    2532
  ],
  "image_file": "item1.png"
}
```

---

## 3. Ba mẫu thật + giải thích

> **Cách đọc:** trên ảnh, **ô viền đỏ** = vị trí nút đúng (do dataset đánh dấu); **chấm xanh** = ví dụ điểm-bấm.
> *Ba ví dụ thuộc 3 nền tảng khác nhau (điện thoại / máy tính / web).*

### Ví dụ 1 — nền tảng: mobile (ios)

![ScreenSpot ví dụ 1](../dataset_samples/screenspot/item1.png)

**Dữ liệu thật:** câu lệnh **“invert the lens”** · loại **icon** · nền **ios** · ô vị trí đúng (pixel) **[965, 2105, 1110, 2258]** trên ảnh **1170×2532**.

**Giải thích (dễ hiểu):** Mẫu này (trên **mobile**) yêu cầu làm thao tác **“invert the lens”**. Dataset đã **đánh dấu sẵn ô chứa nút đúng** (ô viền đỏ, nằm ở **phía dưới bên phải** màn hình). **Cách em dùng:** em cho công cụ chấm-vị-trí của mình chỉ ra *điểm cần bấm*; nếu điểm đó rơi **trong ô đỏ** thì tính là chấm ĐÚNG. Chạy hết ~1.272 mẫu → ra con số *“bộ chấm-vị-trí của em chính xác X%”*. Vì ScreenSpot **đã được công nhận**, con số đó là **bằng chứng đáng tin** cho phần chấm của em.

---

### Ví dụ 2 — nền tảng: desktop (windows)

![ScreenSpot ví dụ 2](../dataset_samples/screenspot/item2.png)

**Dữ liệu thật:** câu lệnh **“close”** · loại **icon** · nền **windows** · ô vị trí đúng (pixel) **[910, 78, 954, 112]** trên ảnh **960×540**.

**Giải thích (dễ hiểu):** Mẫu này (trên **desktop**) yêu cầu làm thao tác **“close”**. Dataset đã **đánh dấu sẵn ô chứa nút đúng** (ô viền đỏ, nằm ở **phía trên bên phải** màn hình). **Cách em dùng:** em cho công cụ chấm-vị-trí của mình chỉ ra *điểm cần bấm*; nếu điểm đó rơi **trong ô đỏ** thì tính là chấm ĐÚNG. Chạy hết ~1.272 mẫu → ra con số *“bộ chấm-vị-trí của em chính xác X%”*. Vì ScreenSpot **đã được công nhận**, con số đó là **bằng chứng đáng tin** cho phần chấm của em.

---

### Ví dụ 3 — nền tảng: web (gitlab)

![ScreenSpot ví dụ 3](../dataset_samples/screenspot/item3.png)

**Dữ liệu thật:** câu lệnh **“create a new project”** · loại **text** · nền **gitlab** · ô vị trí đúng (pixel) **[2321, 129, 2529, 199]** trên ảnh **2560×1440**.

**Giải thích (dễ hiểu):** Mẫu này (trên **web**) yêu cầu làm thao tác **“create a new project”**. Dataset đã **đánh dấu sẵn ô chứa nút đúng** (ô viền đỏ, nằm ở **phía trên bên phải** màn hình). **Cách em dùng:** em cho công cụ chấm-vị-trí của mình chỉ ra *điểm cần bấm*; nếu điểm đó rơi **trong ô đỏ** thì tính là chấm ĐÚNG. Chạy hết ~1.272 mẫu → ra con số *“bộ chấm-vị-trí của em chính xác X%”*. Vì ScreenSpot **đã được công nhận**, con số đó là **bằng chứng đáng tin** cho phần chấm của em.

---

# Tóm tắt (chốt với thầy)

| Dataset | Bình duyệt? | Một item gồm | Đã đưa | Dùng để |
|--|--|--|--|--|
| MobileViews | Preprint (nguồn ảnh/nhãn) | ảnh + bảng nút (view-hierarchy) + XML | 3 màn thật | Nhánh 1 ảnh: chấm chỉ-đúng-nút & không-bịa |
| AndroidControl | ✓ NeurIPS 2024 | mục tiêu + các bước (ảnh + thao tác đúng) | 3 quy trình (3/5/9 bước) | Nhánh nhiều ảnh: xáo trộn → AI sắp lại → chấm τ-b |
| ScreenSpot | ✓ ACL 2024 / ICLR 2025 | ảnh + câu lệnh + ô vị trí đúng | 3 mẫu (di động/máy tính/web) | Đối chứng: bộ chấm-vị-trí của em chính xác % |

*Toàn bộ file gốc ở thư mục `dataset_samples/`. Dữ liệu đã đối chiếu khớp 100% với nguồn — không có gì tự bịa.*