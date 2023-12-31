#ifndef RECV_QUEUE_HPP
#define RECV_QUEUE_HPP

#include <memory>
#include <vector>
#include <unordered_map>
#include <string>
#include "announcement.hpp"

class RecvQueue {
protected:
    std::unordered_map<unsigned short int, std::vector<std::shared_ptr<Announcement>>> _info;

public:
    RecvQueue(int max_prefix_block_id);

    void add_ann(const std::shared_ptr<Announcement>& ann);

    const std::unordered_map<unsigned short int, std::vector<std::shared_ptr<Announcement>>>& prefix_anns() const;

    const std::vector<std::shared_ptr<Announcement>>& get_ann_list(const unsigned short int prefix_block_id) const;
};

#endif // RECV_QUEUE_HPP
