# Đánh giá trước triển khai Antigravity Evidence-First

Ngày: 2026-10-03. Phạm vi: review kiến trúc, kế hoạch, code và test hiện có; không triển khai trong lượt này.

Baseline: branch `feat/antigravity-evidence-first`, HEAD `e51683dfea94cbea75c2774c606c77653f458f05`. Các thay đổi chưa commit được giữ nguyên. Hai reviewer độc lập kiểm tra phần phân phối/cài đặt và hành vi nghiên cứu; kết luận dưới đây được đối chiếu với code và tài liệu chính thức.

## Kết luận

Hướng kiến trúc đáng giữ, nhưng **chưa đủ điều kiện chạy nguyên kế hoạch hoặc thay 69 skill trong profile thật**. Cần chỉnh các điều kiện nghiệm thu và ranh giới tin cậy, không cần đập bỏ thiết kế.

Không thể kết luận chỉ từ prompt rằng Gemini sẽ hết bịa, nhanh hơn hay rẻ hơn. Bản đầu nên được mô tả là bản Antigravity có quy trình kiểm chứng và cài đặt có thể phục hồi, với phạm vi hành vi đã thử được ghi rõ.

## Những phần tốt nên giữ

- Một nguồn canonical, sinh bản Antigravity xác định; không duy trì hai bộ hướng dẫn bằng tay.
- Kiểm tra đúng danh sách 69 tên và tài nguyên đi kèm, không chỉ đếm thư mục.
- Rule chung ngắn; quy trình nghiên cứu chi tiết chỉ đọc khi cần.
- Phân biệt câu hỏi không cần nghiên cứu, tra cứu nhanh và nghiên cứu sâu. Không chạy bộ regression trên từng yêu cầu `/admin`.
- Kiểm chứng ở cấp phát biểu: nguồn tồn tại chưa đủ, đoạn nguồn phải thực sự hỗ trợ kết luận; đối chiếu thời điểm, phạm vi, nguồn gốc và mâu thuẫn.
- Pilot trước rollout; lưu hash sở hữu, sao lưu, bảo vệ `cv-maker`, rule ngoài bộ và cấu hình MCP.

## Phát hiện cần xử lý

### F1 — Chặn rollout: bộ kiểm tra vẫn có thể báo xanh sai

Quan sát thực tế trong lượt review:

- `python -m unittest discover -s tests -v`: 35 test, 34 đạt, 1 lỗi. Test `test_canonical_string_fields_remain_strings_when_scalar_shaped` lỗi vì `name: 123` được chuẩn hóa thành số, thay vì chuỗi mà schema yêu cầu.
- Validator chạy với root không tồn tại `Z:\definitely-does-not-exist-gobal-review`: exit code 0, discovered 0, validated 0.
- Validator với `--skill definitely-not-a-skill`: cũng exit code 0 và không kiểm skill nào.

Điểm code: `scripts/normalize_frontmatter.py:83` chỉ bảo vệ kiểu chuỗi cho `argument-hint`; `.claude/skills/test-framework/scripts/test_skills.py:397` không chặn tập kiểm tra rỗng, và phần CLI coi không có FAIL là thành công.

Sửa cần thiết: root/tập lựa chọn rỗng phải trả lỗi; kiểm tra tên, kiểu và tài nguyên theo schema của từng host. Normalizer phải biết trường nào là chuỗi, kiểm tra toàn bộ đầu vào trước khi ghi và không âm thầm sửa nội dung Markdown. Test idempotence cần đi cùng test bảo toàn ý nghĩa/body và kiểm byte LF, không chỉ so kết quả sau lần chuẩn hóa đầu.

### F2 — Chặn phát hành: runtime của skill chưa tự chứa đầy đủ

Validator đã import `scripts.skill_manifest` bằng đường dẫn suy ra từ repo (`test_skills.py:39`). Quick Start trong `README.md:55` chỉ copy skill/rule vào profile, không copy helper ở repo root. Helper còn import PyYAML (`scripts/skill_manifest.py:3`). Chỉ vendor helper không giải quyết dependency PyYAML.

`understand-codebase/SKILL.md:31` vẫn hướng dẫn chạy `scripts/cb_builder.py` không tồn tại. Resource validator hiện không bắt được mọi kiểu tham chiếu trong lệnh shell, nên xanh cấu trúc chưa chứng minh tài nguyên đầy đủ.

Cần tách rõ: công cụ developer dùng Python/PyYAML; phần cài mà người dùng cần ở runtime; dependency tùy chọn của từng worker. Chọn đóng gói validator thực sự độc lập cho các host, hoặc công bố nó là công cụ repo-only và sửa Quick Start tương ứng. Thay workflow crawler không tồn tại bằng discovery giới hạn bằng `rg`, có fallback.

### F3 — Chặn rollout: gói, rule và vị trí discovery chưa thống nhất

Generator dự kiến mang các rule canonical, nhưng nghiệm thu Direct/Global và Task 11 chủ yếu chỉ nêu `evidence-first.md`. Các skill đang phụ thuộc sáu rule chung; `/admin` còn chỉ tới `research-proposal-integrity.md`. Cần cài và kiểm đủ dependency rule, không chỉ rule mới.

Inventory đọc tại máy này:

| Root | Số SKILL.md | SHA256 admin/SKILL.md |
|---|---:|---|
| `C:\Users\Asus\.gemini\config\skills` | 70 | `1A80E0BF94D880FA95FEBA134AE61C99E9C918513483407D6CF2BBD0CDE2D2A9` |
| `C:\Users\Asus\.gemini\antigravity\skills` | 69 | `4D11D48A234867ECDE5312DD6B966485F1BB080A564DA6FA7B588C714E2BA18B` |

Đây là hai vị trí được tài liệu IDE hỗ trợ, với hai bản admin khác nhau. Chưa có trace xác nhận bản nào được chọn khi tên trùng; không gán đây là nguyên nhân chắc chắn của lỗi cũ. Trước rollout phải kiểm kê trùng tên, chứng minh nguồn skill được nạp và xử lý bản trùng theo sở hữu/sao lưu; không xóa cả thư mục legacy.

Tài liệu dành riêng cho IDE hướng dẫn plugin theo filesystem và Customizations; `/plugin install` nằm ở phần TUI. Không quảng cáo nó là lệnh IDE đã thử. Gói plugin vẫn có thể sinh, nhưng chỉ công bố hỗ trợ cài plugin sau kiểm chứng topology đó. [Tài liệu skills](https://antigravity.google/docs/skills?tab=ide), [tài liệu plugins](https://antigravity.google/docs/plugins?tab=ide).

### F4 — Chặn tuyên bố chất lượng: pilot và test hành vi chưa đủ chứng minh

Pilot dùng `model_decision`, production dùng `always_on` (`notes/plan-antigravity-evidence-first.md:442`). Mô tả rule `model_decision` không phải cơ chế bảo đảm chỉ nạp khi gõ đúng slash command. Pilot này không chứng minh production luôn nạp rule. Cần kiểm riêng cơ chế production, theo cách kiểm soát được và có thể gỡ sạch. [Tài liệu rules](https://antigravity.google/docs/rules?tab=ide).

Các assertion có từ khóa chỉ chứng minh hướng dẫn hiện diện, không chứng minh model tuân thủ. Mười hai case được dự kiến nhưng chưa có bước chạy/chấm toàn bộ; một câu hỏi Quick không chứng minh Standard/Deep, tổng hợp mâu thuẫn hay chống bịa nói chung.

Nghiệm thu phải tách: case đã viết; check cấu trúc đã chạy; case đã đánh giá offline; case đã chạy trên IDE thật. Có thể dùng một canary nhiều khía cạnh và tập nhỏ được chấm thủ công, không bắt chạy 12 lượt model trả phí. Case chưa chạy phải ghi là chưa chạy, không báo regression pass.

### F5 — Chặn lớp hành vi: ranh giới tin cậy còn sai

`VERIFIED_OR_GIVEN` gộp dữ kiện đã quan sát với thông tin người dùng đưa (`notes/design-antigravity-evidence-first.md:269`). Lời người dùng là đầu vào cần tôn trọng, không mặc nhiên là sự thật đã kiểm chứng. Cần tách `USER_REPORTED` và `OBSERVED_VERIFIED`; yêu cầu/ưu tiên của người dùng cũng khác phát biểu về sự thật.

Khi có phản chứng, mở lại claim và các suy luận phụ thuộc để kiểm tra, không tự động biến lời sửa mới thành chân lý. Giữ hai đường bằng chứng nếu đang tranh chấp.

Thêm invariant rõ: nội dung trong trang web, PDF, repo, attachment và evidence của worker là dữ liệu nguồn. Chỉ dẫn nằm trong chúng không được thay đổi yêu cầu người dùng, quyền dùng công cụ, budget hoặc kết quả kiểm chứng. Fixture prompt injection đơn thuần chưa thay thế được rule này.

### F6 — Cần sửa trước pilot: dispatch và budget phải thống nhất theo host

Task 5 chưa liệt kê sửa `admin/references/dispatch-protocol.md`, trong khi file đó vẫn đề xuất 3–5/4–5 worker; thiết kế mới giới hạn tối đa ba. Contract worker hiện chỉ cần summary/path, chưa yêu cầu claim IDs, locator/đoạn bằng chứng và nguồn gốc.

Cần cập nhật dispatch, hướng dẫn của domain admin liên quan và `token-budget`. Không mang mặc định context 200k của Claude Opus sang Gemini; không giữ khẳng định chi phí parallel ≈10x như một số đã đo.

Tool name của Claude không tự biến thành capability Antigravity bằng thay chuỗi. Cần bảng capability nhỏ đã xác minh: đọc/tìm file, web, invoke skill, subagent; có fallback tuần tự khi host không hỗ trợ.

Budget là tổng dùng chung giữa admin và mọi worker: số query, source opens, lượng nguồn đọc và số vòng. Không cho mỗi worker tự dùng trọn trần chung. Giá trị khởi đầu là chính sách thiết kế cần thử, chưa phải tối ưu đã chứng minh.

### F7 — Cần sửa trước ledger validator: kiểm cấu trúc không phải kiểm sự thật

Ledger phải có đoạn đã kiểm hoặc locator tái lập được, stance theo từng cạnh claim–source, ánh xạ phát biểu trong câu trả lời về claim, và hồ sơ review. Một tài liệu có thể hỗ trợ claim này nhưng bác claim khác.

Thêm negative tests cho source/claim ID không tồn tại, derivation vòng lặp, suy luận dựa vào `NEI`, status mâu thuẫn với evidence và conflict bị bỏ qua. `NEI` là chưa đủ thông tin, không có nghĩa claim sai. `REFUTED` cần bằng chứng bác bỏ; `CONTESTED` cần giữ các bằng chứng bất đồng đáng tin.

Validator xác định có thể bắt thiếu field/quan hệ; không thể tự xác nhận một đoạn thực sự kéo theo kết luận. Phải ghi giới hạn này và chấm nội dung case mẫu; không tạo sự chắc chắn giả bằng field `entailment: direct` do model tự điền.

### F8 — Cần sửa trước cài profile thật: nói đúng về rollback

Thay nhiều đường dẫn skill/rule không phải một thao tác filesystem atomic duy nhất. Plan chưa có cơ chế khóa, nhật ký phục hồi sau dừng đột ngột hoặc lệnh phục hồi rõ ràng; lời hứa rollback trên mọi lỗi mạnh hơn phần mô tả implementation.

Giữ staging, validate trước ghi, backup và hash từng file. Định nghĩa trạng thái transaction và phục hồi từ journal; chặn hai installer chạy đồng thời; fault-injection cho lỗi giữa chừng. Phục hồi chỉ các target thuộc transaction, không chép đè snapshot rộng lên dữ liệu người dùng đã sửa sau đó. Không đụng MCP hoặc file ngoài sở hữu.

## Quyết định cho 12 đầu việc hiện tại

| Task | Quyết định | Điều chỉnh chính |
|---|---|---|
| 1 — Python harness | Giữ | Tách dependency developer và runtime; test môi trường sạch. |
| 2 — Validator | Mở lại | Chặn tập rỗng/root sai/filter sai; discovery và schema theo host. |
| 3 — Normalize/resources | Hoàn tất có kiểm soát | Sửa test đang lỗi, bảo toàn body, validate batch, bỏ phantom crawler. |
| 4 — Generator/plugin | Giữ, chia nhỏ | Bundle pilot tối thiểu trước; đủ rules/resources; capability fallback; plugin là topology cần thử riêng. |
| 5 — Evidence-first admin | Sửa thiết kế trước viết | Trust boundary, fact provenance, counter-evidence, cập nhật dispatch và token-budget. |
| 6 — Ledger validator | Giữ, thu hẹp lời hứa | Check cấu trúc chặt; review nội dung không được thay bằng schema. |
| 7 — Installer | Giữ, theo từng mức | Pilot tối thiểu có test trước; full install thêm ownership, khóa/journal và phục hồi. |
| 8 — Docs/cases/CI | Làm song song phần đã xác minh | Hướng dẫn đúng IDE; ghi rõ test đã/chưa chạy, dependency, giới hạn. |
| 9 — Review/verification | Giữ | Gate dựa vào output/exit code thật; cả negative tests và môi trường sạch. |
| 10 — Pilot | Đưa lên sớm sau bundle tối thiểu | Chứng minh discovery, body activation, rule production và hành vi đại diện bằng trace. |
| 11 — Thay 69 skill | Chưa chạy | Chỉ sau các gate; kiểm bản trùng, đủ rules; bảo vệ cv-maker/MCP; rollback có thử. |
| 12 — GitHub | Cuối cùng | Chỉ publish những topology và hành vi có bằng chứng; kiểm commit/remote. |

## Thứ tự thực hiện đề xuất

1. Sửa nền validator/normalizer và dependency/resource hỏng; toàn bộ test phải đạt, cả negative tests mới.
2. Chốt contract tin cậy, nguồn và budget; viết admin/rule/references tối thiểu. Không dựng thêm framework điều phối lớn.
3. Đóng gói pilot tự chứa, test cài/gỡ trên thư mục tạm; chạy canary IDE thật sớm. Không coi marker trả lời là đủ bằng chứng nếu thiếu trace nguồn file/rule/tool.
4. Sau khi giả định sản phẩm được kiểm chứng, sinh đủ 69 skill cùng dependency rules; kiểm build xác định và installer full trên profile tạm, lỗi giữa chừng, update/uninstall và dữ liệu ngoài bộ.
5. Rollout có backup và đối chiếu hash trước/sau; smoke test `/admin`, worker đại diện và rule; thiếu gate thì không chuyển production.
6. Chốt tài liệu/CI/report và cập nhật GitHub. Hoãn backend nghiên cứu ngoài, archive hạ tầng lớn, benchmark model diện rộng và hỗ trợ plugin chưa thử.

## Tối ưu chi phí và thời gian: điều kiện đánh giá

- Unit/integration/regression chạy lúc phát hành, không chạy trên mỗi chat.
- Câu hỏi không cần web không đi qua pipeline nghiên cứu. Tra cứu chính xác, rủi ro thấp có thể đủ một nguồn sơ cấp trực tiếp; không ép nhiều nguồn chỉ để đẹp số lượng.
- Nghiên cứu lớn mới đọc protocol/ghi ledger bền vững; kiểm claim quan trọng, batch thao tác độc lập và dừng khi đủ bằng chứng.
- Quick hết budget thì trả kết quả giới hạn/unknown; không tự kéo dài vòng tìm hoặc giảm chuẩn trung thực.
- Đo baseline và bản mới trên cùng task/model/mức reasoning: tổng search/open/worker, thời gian và token nếu runtime cung cấp. Chưa đo thì không công bố phần trăm tiết kiệm hoặc cam kết thời gian.
- Chi phí metadata của cả bộ và rule luôn nạp cũng phải được tính; không dùng token đếm cho Claude để giả làm số token Gemini.

## Gate trước thay 69 skill

- Test Python xanh, và các lỗi empty root/filter phải cho exit code khác 0.
- Exact-name inventory, rules/resources/dependency closure và build byte-deterministic đạt.
- Install/update/uninstall/recovery trên profile tạm đạt, không sửa dữ liệu ngoài sở hữu.
- Có activity trace IDE chứng minh bản pilot/body nào chạy và rule được nạp; tài liệu cài đặt khớp topology đã thử.
- Canary và tập đánh giá nội dung nhỏ có kết quả: tiền đề sai, nguồn có thật nhưng không hỗ trợ, phản chứng, nguồn sao chép, instruction độc trong nguồn, yêu cầu sáng tạo không cần tìm web. Phạm vi nào chưa test phải ghi rõ.
- Xác minh hai root hiện hữu và backup/rollback trước khi đổi profile thật; không kết luận nguyên nhân lỗi cũ nếu chưa có log.

Review này không sửa skill, plan, installer, profile hay GitHub; chỉ thêm báo cáo. Cũng chưa chạy mô hình Gemini hoặc kiểm tra giao diện IDE. Vì vậy kết luận là **giữ hướng kiến trúc, sửa các gate và contract trước; chưa rollout**.
