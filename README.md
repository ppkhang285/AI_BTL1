## Luật chơi Masyu (Có ảnh minh họa trong folder)
- Bàn 6x6 gồm các điểm, có thể chứa các vòng tròn trắng và đen
- Nhiệm vụ: Vẽ 1 đường thẳng đi qua tất cả vòng tròn, không được rẽ nhánh và nằm lên nhau. -> Điểm đích chính là điểm ban đầu
- Luật vẽ đường thẳng:
- Vòng tròn trẳng phải đi qua bằng đường thẳng, và phải rẽ trước hoặc sau đó
- vòng tròn đen phải rẽ, và phải đi thẳng trước và sau đó
## Nguyên văn luật: https://www.puzzle-masyu.com/
The rules are simple. You have to draw lines between the dots to form a single loop without crossings or branches. The loop should pass through all black and white circles in such a way that:
- White circles must be passed through in a straight line, but the loop must turn in the previous and/or the next cell.
- Black circles must be turned upon and the loop must travel straight through the next and the previous cell.
## How to USE
- Chạy DFS: "python .\Masyu_DFS.py <testcase>"
- Chạy A*: "python .\Masyu_A.py <testcase>"
- Chạy demo: "python .\Demo.py"
## Note
* \<testcase\>: số 1, 2 hoặc 3
* Nếu bị lỗi đọc file trong Demo: Chạy DFS và A* của testcase đó trước
* By some way DFS chạy nhanh hơn A*

## DFS
- Đơn giản là di chuyển theo 4 hướng rồi check luật và điều kiện chiến thắng
## A*
- Hàm h(x) = (khoảng cách Mahathan điểm hiện đại đến điểm đích(điểm ban đầu) )+ (số ô trắng và đen chưa đi qua) * 2
 = dis(current, goal) + circleCount *2
- g(x) = số điểm đã đi qua
- f(x) = h(x) + g(x)
- State bao gồm: path(đường đã đi) và circleCount(số ô trắng/đen chưa khám phá)
